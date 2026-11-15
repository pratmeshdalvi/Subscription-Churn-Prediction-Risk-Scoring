--Task 1: Calculate overall churn rate
SELECT
    COUNT(*) AS total_customers,

    COUNT(*) FILTER (
        WHERE churn_flag = 1
    ) AS churned_customers,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE churn_flag = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate

FROM churn_events;

--Task 2: Churn by subscription plan

SELECT
    s.plan,

    COUNT(*) AS total_customers,

    COUNT(*) FILTER (
        WHERE c.churn_flag = 1
    ) AS churned_customers,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE c.churn_flag = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate

FROM subscriptions s

JOIN churn_events c
    ON s.customer_id = c.customer_id

GROUP BY s.plan
ORDER BY churn_rate DESC;

--Task 3: Churn by billing cycle
SELECT
    s.billing_cycle,

    COUNT(*) AS total_customers,

    COUNT(*) FILTER (
        WHERE c.churn_flag = 1
    ) AS churned_customers,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE c.churn_flag = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate

FROM subscriptions s

JOIN churn_events c
    ON s.customer_id = c.customer_id

GROUP BY s.billing_cycle
ORDER BY churn_rate DESC;

--Task 4: Churn by region
SELECT
    cu.region,
    COUNT(*) AS total_customers,

    COUNT(*) FILTER (
        WHERE ch.churn_flag = 1
    ) AS churned_customers,

    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE ch.churn_flag = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate

FROM customers cu

JOIN churn_events ch
    ON cu.customer_id = ch.customer_id

GROUP BY cu.region
ORDER BY churn_rate DESC;

--Task 5: Churn reasons
SELECT
    churn_reason,
    COUNT(*) AS customers
FROM churn_events
WHERE churn_flag = 1
GROUP BY churn_reason
ORDER BY customers DESC;

--Task 6: Churn by tenure group
WITH customer_tenure AS (
    SELECT 
        s.customer_id,
        (COALESCE(s.end_date, DATE '2025-12-31') - s.start_date) / 30.0 AS tenure_months,
        c.churn_flag
    FROM subscriptions s
    JOIN churn_events c ON s.customer_id = c.customer_id
)
SELECT 
    CASE 
        WHEN tenure_months < 3 THEN '0-3 Months'
        WHEN tenure_months < 6 THEN '3-6 Months'
        WHEN tenure_months < 12 THEN '6-12 Months'
        ELSE '12+ Months'
    END AS tenure_group,
    COUNT(*) AS customers,
    ROUND(
        100.0 * SUM(churn_flag) / NULLIF(COUNT(*), 0), 
        2
    ) AS churn_rate
FROM customer_tenure
GROUP BY tenure_group
ORDER BY churn_rate DESC;


