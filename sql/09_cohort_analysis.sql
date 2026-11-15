WITH usage_summary AS (
    SELECT
        customer_id,
        ROUND(AVG(usage_hours), 2) AS avg_usage_hours,
        ROUND(AVG(sessions_count), 2) AS avg_sessions,
        ROUND(AVG(active_days), 2) AS avg_active_days
    FROM usage_activity
    GROUP BY customer_id
),

payment_summary AS (
    SELECT
        customer_id,
        COUNT(*) AS total_payments,
        COUNT(*) FILTER (
            WHERE payment_status = 'Failed'
        ) AS failed_payments
    FROM payments
    GROUP BY customer_id
),

support_summary AS (
    SELECT
        customer_id,
        COUNT(*) AS total_tickets,
        ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time,
        ROUND(AVG(satisfaction_score), 2) AS avg_satisfaction
    FROM support_tickets
    GROUP BY customer_id
)

SELECT
    c.customer_id,
    c.region,
    c.acquisition_channel,

    s.plan,
    s.billing_cycle,
    ROUND(s.monthly_fee, 2) AS monthly_fee,

    u.avg_usage_hours,
    u.avg_sessions,
    u.avg_active_days,

    p.total_payments,
    p.failed_payments,

    ROUND(
        CASE
            WHEN p.total_payments > 0
            THEN p.failed_payments::NUMERIC / p.total_payments
            ELSE 0
        END, 
        2
    ) AS payment_failure_rate,

    sp.total_tickets,
    sp.avg_resolution_time,
    sp.avg_satisfaction,

    ch.churn_flag

FROM customers c
LEFT JOIN subscriptions s
    ON c.customer_id = s.customer_id
LEFT JOIN usage_summary u
    ON c.customer_id = u.customer_id
LEFT JOIN payment_summary p
    ON c.customer_id = p.customer_id
LEFT JOIN support_summary sp
    ON c.customer_id = sp.customer_id
LEFT JOIN churn_events ch
    ON c.customer_id = ch.customer_id;
