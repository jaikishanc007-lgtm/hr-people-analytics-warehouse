-- ============================================================
-- HR Data Warehouse — Analytics Queries
-- Author: Jaiki
-- Database: hr_warehouse (PostgreSQL 18)
-- ============================================================


-- ── 1. EXECUTIVE KPI SUMMARY ─────────────────────────────
SELECT
    COUNT(*) FILTER (WHERE "Attrition" = 'No')        AS active_headcount,
    COUNT(*) FILTER (WHERE "Attrition" = 'Yes')       AS attrited_employees,
    ROUND(COUNT(*) FILTER (WHERE "Attrition" = 'Yes')
          * 100.0 / COUNT(*), 1)                      AS attrition_rate_pct,
    ROUND(AVG("BaseSalary")::numeric, 0)               AS avg_base_salary,
    ROUND(AVG("EngagementScore")::numeric, 1)          AS avg_engagement,
    ROUND(AVG("BurnoutScore")::numeric, 1)             AS avg_burnout,
    ROUND(SUM("RevenueContribution")::numeric / 1000000, 1) AS total_revenue_millions
FROM fact_employee_history
WHERE "EmployeeID" NOT LIKE '%_DUP';


-- ── 2. ATTRITION BY DEPARTMENT ───────────────────────────
SELECT
    "Department",
    COUNT(*) AS total_employees,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1) AS attrition_rate_pct,
    ROUND(AVG("BaseSalary")::numeric, 0) AS avg_salary,
    ROUND(AVG("BurnoutScore")::numeric, 1) AS avg_burnout
FROM fact_employee_history
WHERE "EmployeeID" NOT LIKE '%_DUP'
GROUP BY "Department"
ORDER BY attrition_rate_pct DESC;


-- ── 3. ATTRITION BY AGE GROUP ────────────────────────────
SELECT
    CASE
        WHEN "Age" < 25 THEN 'Under 25'
        WHEN "Age" BETWEEN 25 AND 34 THEN '25-34'
        WHEN "Age" BETWEEN 35 AND 44 THEN '35-44'
        WHEN "Age" BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS total,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1) AS attrition_rate_pct
FROM fact_employee_history
WHERE "EmployeeID" NOT LIKE '%_DUP'
GROUP BY age_group
ORDER BY attrition_rate_pct DESC;


-- ── 4. ATTRITION BY COUNTRY ──────────────────────────────
SELECT
    "Country",
    COUNT(*) AS total_employees,
    SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS attrited,
    ROUND(SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1) AS attrition_rate_pct,
    ROUND(AVG("BaseSalary")::numeric, 0) AS avg_salary
FROM fact_employee_history
WHERE "EmployeeID" NOT LIKE '%_DUP'
GROUP BY "Country"
ORDER BY attrition_rate_pct DESC;


-- ── 5. ATTRITION REASONS BREAKDOWN ───────────────────────
SELECT
    "AttritionReason",
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 /
          SUM(COUNT(*)) OVER (), 1) AS percentage
FROM fact_employee_history
WHERE "Attrition" = 'Yes'
  AND "AttritionReason" IS NOT NULL
GROUP BY "AttritionReason"
ORDER BY total DESC;


-- ── 6. SALARY ANALYSIS BY JOB LEVEL ─────────────────────
SELECT
    "JobLevel",
    "LevelLabel",
    COUNT(*) AS headcount,
    ROUND(AVG("BaseSalary")::numeric, 0) AS avg_salary,
    ROUND(MIN("BaseSalary")::numeric, 0) AS min_salary,
    ROUND(MAX("BaseSalary")::numeric, 0) AS max_salary,
    ROUND(AVG("BonusPercent")::numeric, 1) AS avg_bonus_pct
FROM fact_employee_history
WHERE "EmployeeID" NOT LIKE '%_DUP'
GROUP BY "JobLevel", "LevelLabel"
ORDER BY "JobLevel";


-- ── 7. MANAGER EFFECT ON ATTRITION ───────────────────────
SELECT
    m."ManagerName",
    m."Department",
    COUNT(e."EmployeeID") AS team_size,
    ROUND(AVG(e."ManagerRating")::numeric, 2) AS avg_mgr_rating,
    ROUND(AVG(CASE WHEN e."Attrition" = 'Yes'
              THEN 1.0 ELSE 0 END) * 100, 1) AS team_attrition_pct
FROM dim_managers m
JOIN fact_employee_history e ON e."ManagerID" = m."ManagerID"
WHERE e."EmployeeID" NOT LIKE '%_DUP'
GROUP BY m."ManagerName", m."Department"
HAVING COUNT(e."EmployeeID") >= 5
ORDER BY team_attrition_pct DESC
LIMIT 20;


-- ── 8. TRAINING IMPACT ON PERFORMANCE ───────────────────
SELECT
    CASE
        WHEN "TrainingHours" < 20  THEN 'Low (under 20h)'
        WHEN "TrainingHours" < 60  THEN 'Medium (20-60h)'
        ELSE 'High (60h+)'
    END AS training_band,
    COUNT(*) AS employees,
    ROUND(AVG("PerformanceRating")::numeric, 2) AS avg_performance,
    ROUND(AVG(CASE WHEN "Attrition" = 'Yes'
              THEN 1.0 ELSE 0 END) * 100, 1) AS attrition_pct
FROM fact_employee_history
WHERE "TrainingHours" IS NOT NULL
  AND "EmployeeID" NOT LIKE '%_DUP'
GROUP BY training_band
ORDER BY avg_performance DESC;


-- ── 9. HIGH RISK EMPLOYEES ───────────────────────────────
SELECT
    "EmployeeID",
    "EmployeeName",
    "Department",
    "JobLevel",
    "Country",
    "AttritionRiskScore",
    "BurnoutScore",
    "JobSatisfactionScore",
    "EngagementScore",
    "OvertimeHoursPerMonth"
FROM fact_employee_history
WHERE "Attrition" = 'No'
  AND "EmployeeID" NOT LIKE '%_DUP'
  AND "AttritionRiskScore" >= 70
ORDER BY "AttritionRiskScore" DESC
LIMIT 50;


-- ── 10. DIVERSITY RATIO BY COUNTRY ──────────────────────
SELECT
    "Country",
    COUNT(*) AS total,
    SUM(CASE WHEN "Gender" = 'Female' THEN 1 ELSE 0 END) AS female,
    SUM(CASE WHEN "Gender" = 'Male' THEN 1 ELSE 0 END) AS male,
    ROUND(SUM(CASE WHEN "Gender" = 'Female' THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1) AS female_pct
FROM fact_employee_history
WHERE "EmployeeID" NOT LIKE '%_DUP'
GROUP BY "Country"
ORDER BY female_pct DESC;
