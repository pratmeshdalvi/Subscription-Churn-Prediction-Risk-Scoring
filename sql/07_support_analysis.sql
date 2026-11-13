--Task 1: Most common customer complaints
select * from support_tickets;
SELECT
    issue_type,
    COUNT(*) AS total_tickets
FROM support_tickets
GROUP BY issue_type
ORDER BY total_tickets DESC;

--Task 2: Average resolution time
SELECT
    issue_type,
    ROUND(
        AVG(resolution_time_hours), 2
    ) AS avg_resolution_hours
FROM support_tickets
GROUP BY issue_type;

--Task 3: Satisfaction by issue type

SELECT
    issue_type,
    ROUND(
        AVG(satisfaction_score), 2
    ) AS avg_satisfaction
FROM support_tickets
GROUP BY issue_type;

--Task 4: Customers with repeated complaints
SELECT 
    customer_id, 
    COUNT(*) AS ticket_count, 
    ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_time, 
    Round(AVG(satisfaction_score),2) AS avg_satisfaction 
FROM support_tickets 
GROUP BY customer_id 
HAVING COUNT(*) >= 3;

