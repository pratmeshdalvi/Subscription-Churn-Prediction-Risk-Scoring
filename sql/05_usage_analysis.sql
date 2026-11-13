--Task 1: Average usage by customer
select *  from customers;
SELECT
    customer_id,
    ROUND(AVG(usage_hours), 2) AS avg_usage,
    ROUND(AVG(sessions_count), 2) AS avg_sessions,
    ROUND(AVG(active_days), 2) AS avg_active_days
FROM usage_activity
GROUP BY customer_id;

--Task 2: Identify low-engagement customers
select * from usage_activity;
SELECT
    customer_id,
    AVG(usage_hours) AS avg_usage
FROM usage_activity
GROUP BY customer_id
HAVING AVG(usage_hours) < 10;

--Task 3: Monthly usage trend
SELECT
    activity_month,
    SUM(sessions_count) AS total_sessions,
    SUM(usage_hours) AS total_usage_hours,
    AVG(active_days) AS avg_active_days
FROM usage_activity
GROUP BY activity_month
ORDER BY activity_month;

--Task 4: Engagement trend using window functions


WITH usage_trend AS (
    SELECT
        customer_id,
        activity_month,
        usage_hours,

        LAG(usage_hours) OVER (
            PARTITION BY customer_id
            ORDER BY activity_month
        ) AS previous_month_usage

    FROM usage_activity
)

SELECT
    customer_id,
    activity_month,
    usage_hours,
    previous_month_usage,
    usage_hours - previous_month_usage AS usage_change

FROM usage_trend;

