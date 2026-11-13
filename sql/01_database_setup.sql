CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE,
    age_group VARCHAR(20),
    gender VARCHAR(20),
    region VARCHAR(50),
    acquisition_channel VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    plan VARCHAR(30),
    billing_cycle VARCHAR(20),
    start_date DATE,
    end_date DATE,
    monthly_fee NUMERIC(10,2),
    discount_pct NUMERIC(5,2),
    auto_renew BOOLEAN,
    subscription_status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS usage_activity (
    activity_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    activity_month DATE,
    sessions INT,
    usage_hours NUMERIC(10,2),
    active_days INT,
    features_used INT,
    last_login_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    payment_date DATE,
    amount NUMERIC(10,2),
    payment_status VARCHAR(20),
    payment_method VARCHAR(30),
    failure_reason VARCHAR(100),
    days_late INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    ticket_date DATE,
    issue_type VARCHAR(50),
    priority VARCHAR(20),
    resolution_time_hours NUMERIC(10,2),
    satisfaction_score INT,
    ticket_status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS churn_events (
    customer_id VARCHAR(20) PRIMARY KEY,
    churn_flag INT CHECK (churn_flag IN (0,1)),
    churn_date DATE,
    churn_reason VARCHAR(100),
    cancellation_channel VARCHAR(30),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
