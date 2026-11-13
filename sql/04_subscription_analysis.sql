--Task 1: Plan distribution
SELECT
    plan,
    COUNT(*) AS total_subscriptions
FROM subscriptions
GROUP BY plan
ORDER BY total_subscriptions DESC;

--Task 2: Average subscription price

SELECT
    plan,
    ROUND(AVG(monthly_fee), 2) AS avg_monthly_fee
FROM subscriptions
GROUP BY plan;

--Task 3: Plan versus billing cycle
SELECT
    plan,
    billing_cycle,
    COUNT(*) AS customers
FROM subscriptions
GROUP BY plan, billing_cycle
ORDER BY plan, customers DESC;

--Task 4: Subscription tenure
SELECT
    subscription_id,
    customer_id,
    plan,
    AGE(
        COALESCE(end_date, CURRENT_DATE),
        start_date
    ) AS subscription_duration
FROM subscriptions;
