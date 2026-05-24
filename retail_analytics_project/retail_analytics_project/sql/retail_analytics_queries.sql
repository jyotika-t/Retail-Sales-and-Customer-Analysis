-- =============================================================
-- RETAIL SALES & CUSTOMER ANALYTICS PROJECT
-- SQL Queries — MySQL Compatible
-- =============================================================
-- How to use:
--   Option A) MySQL Workbench  → Run all queries below
--   Option B) DB Fiddle        → https://www.db-fiddle.com
--             Choose MySQL 8.0, paste CREATE TABLE + INSERT,
--             then run SELECT queries in the right pane.
-- =============================================================


-- ── 1. CREATE DATABASE & TABLE ──────────────────────────────

CREATE DATABASE IF NOT EXISTS retail_analytics;
USE retail_analytics;

DROP TABLE IF EXISTS retail_sales;

CREATE TABLE retail_sales (
    row_id          INT,
    order_id        VARCHAR(20),
    order_date      DATE,
    ship_date       DATE,
    ship_mode       VARCHAR(30),
    customer_id     VARCHAR(15),
    customer_name   VARCHAR(60),
    segment         VARCHAR(20),
    country         VARCHAR(30),
    city            VARCHAR(50),
    state           VARCHAR(40),
    postal_code     VARCHAR(10),
    region          VARCHAR(15),
    product_id      VARCHAR(20),
    category        VARCHAR(30),
    sub_category    VARCHAR(30),
    product_name    VARCHAR(255),
    sales           DECIMAL(12, 4)
);

-- ── 2. LOAD DATA (MySQL LOCAL INFILE) ───────────────────────
-- Update the path to your actual file location.
-- Make sure LOCAL_INFILE is enabled:
--   SET GLOBAL local_infile = 1;
-- Then:
LOAD DATA LOCAL INFILE '/path/to/retail_analytics_project/data/cleaned_data.csv'
INTO TABLE retail_sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(row_id, order_id, @order_date, @ship_date, ship_mode, customer_id,
 customer_name, segment, country, city, state, postal_code, region,
 product_id, category, sub_category, product_name, sales,
 @dummy1, @dummy2, @dummy3, @dummy4, @dummy5, @dummy6, @dummy7)
SET order_date = STR_TO_DATE(@order_date, '%Y-%m-%d'),
    ship_date  = STR_TO_DATE(@ship_date,  '%Y-%m-%d');

-- (If using DB Fiddle, skip LOAD DATA and paste sample rows manually)


-- ═══════════════════════════════════════════════════════════
-- ── SECTION A: SALES KPI QUERIES ───────────────────────────
-- ═══════════════════════════════════════════════════════════

-- Q1. Overall KPIs
SELECT
    COUNT(DISTINCT order_id)   AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT product_id) AS total_products,
    ROUND(SUM(sales), 2)       AS total_revenue,
    ROUND(AVG(sales), 2)       AS avg_order_line_value,
    ROUND(MAX(sales), 2)       AS max_single_line_sale,
    ROUND(MIN(sales), 2)       AS min_single_line_sale
FROM retail_sales;


-- Q2. Annual Revenue Summary
SELECT
    YEAR(order_date)           AS year,
    COUNT(DISTINCT order_id)   AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2)       AS revenue,
    ROUND(AVG(sales), 2)       AS avg_order_value
FROM retail_sales
GROUP BY YEAR(order_date)
ORDER BY year;


-- Q3. Month-over-Month Revenue
SELECT
    YEAR(order_date)   AS year,
    MONTH(order_date)  AS month,
    DATE_FORMAT(order_date, '%b %Y') AS period,
    ROUND(SUM(sales), 2) AS monthly_revenue
FROM retail_sales
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;


-- Q4. Quarterly Performance
SELECT
    YEAR(order_date)    AS year,
    QUARTER(order_date) AS quarter,
    ROUND(SUM(sales), 2) AS quarterly_revenue,
    COUNT(DISTINCT order_id) AS orders
FROM retail_sales
GROUP BY YEAR(order_date), QUARTER(order_date)
ORDER BY year, quarter;


-- Q5. Year-over-Year Growth
WITH annual AS (
    SELECT
        YEAR(order_date) AS yr,
        ROUND(SUM(sales), 2) AS revenue
    FROM retail_sales
    GROUP BY YEAR(order_date)
)
SELECT
    yr,
    revenue,
    LAG(revenue) OVER (ORDER BY yr) AS prev_year_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY yr))
        / LAG(revenue) OVER (ORDER BY yr) * 100, 2
    ) AS yoy_growth_pct
FROM annual
ORDER BY yr;


-- ═══════════════════════════════════════════════════════════
-- ── SECTION B: PRODUCT & CATEGORY ANALYSIS ─────────────────
-- ═══════════════════════════════════════════════════════════

-- Q6. Revenue by Category
SELECT
    category,
    COUNT(DISTINCT order_id)    AS orders,
    ROUND(SUM(sales), 2)        AS total_sales,
    ROUND(AVG(sales), 2)        AS avg_sale,
    ROUND(SUM(sales) / (SELECT SUM(sales) FROM retail_sales) * 100, 2) AS pct_of_total
FROM retail_sales
GROUP BY category
ORDER BY total_sales DESC;


-- Q7. Revenue by Sub-Category
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS revenue,
    COUNT(*)              AS transactions,
    ROUND(AVG(sales), 2)  AS avg_sale
FROM retail_sales
GROUP BY category, sub_category
ORDER BY category, revenue DESC;


-- Q8. Top 20 Products by Revenue
SELECT
    product_name,
    category,
    sub_category,
    COUNT(*)              AS times_sold,
    ROUND(SUM(sales), 2)  AS total_revenue,
    ROUND(AVG(sales), 2)  AS avg_price
FROM retail_sales
GROUP BY product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 20;


-- Q9. Bottom 10 Products (underperformers)
SELECT
    product_name,
    category,
    COUNT(*)             AS times_sold,
    ROUND(SUM(sales), 2) AS total_revenue
FROM retail_sales
GROUP BY product_name, category
ORDER BY total_revenue ASC
LIMIT 10;


-- Q10. Pareto — Products Driving 80% Revenue
WITH prod_sales AS (
    SELECT
        product_name,
        ROUND(SUM(sales), 2) AS revenue
    FROM retail_sales
    GROUP BY product_name
    ORDER BY revenue DESC
),
ranked AS (
    SELECT
        product_name,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
        SUM(revenue) OVER ()                      AS total_revenue
    FROM prod_sales
)
SELECT
    product_name,
    revenue,
    ROUND(cumulative_revenue / total_revenue * 100, 2) AS cumulative_pct
FROM ranked
WHERE cumulative_revenue / total_revenue <= 0.80
ORDER BY revenue DESC;


-- ═══════════════════════════════════════════════════════════
-- ── SECTION C: REGIONAL ANALYSIS ───────────────────────────
-- ═══════════════════════════════════════════════════════════

-- Q11. Revenue by Region
SELECT
    region,
    COUNT(DISTINCT order_id)    AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2)        AS total_revenue,
    ROUND(AVG(sales), 2)        AS avg_order_value
FROM retail_sales
GROUP BY region
ORDER BY total_revenue DESC;


-- Q12. Top 15 States by Revenue
SELECT
    state,
    region,
    COUNT(DISTINCT order_id)    AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(sales), 2)        AS revenue
FROM retail_sales
GROUP BY state, region
ORDER BY revenue DESC
LIMIT 15;


-- Q13. Bottom 10 States (underperforming)
SELECT
    state,
    region,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(sales), 2)     AS revenue
FROM retail_sales
GROUP BY state, region
ORDER BY revenue ASC
LIMIT 10;


-- Q14. Top 10 Cities by Revenue
SELECT
    city,
    state,
    region,
    ROUND(SUM(sales), 2) AS revenue,
    COUNT(DISTINCT order_id) AS orders
FROM retail_sales
GROUP BY city, state, region
ORDER BY revenue DESC
LIMIT 10;


-- Q15. Region × Category Breakdown
SELECT
    region,
    category,
    ROUND(SUM(sales), 2)        AS revenue,
    COUNT(DISTINCT customer_id) AS customers
FROM retail_sales
GROUP BY region, category
ORDER BY region, revenue DESC;


-- ═══════════════════════════════════════════════════════════
-- ── SECTION D: CUSTOMER ANALYTICS ──────────────────────────
-- ═══════════════════════════════════════════════════════════

-- Q16. Revenue by Customer Segment
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT order_id)    AS orders,
    ROUND(SUM(sales), 2)        AS revenue,
    ROUND(AVG(sales), 2)        AS avg_order_value
FROM retail_sales
GROUP BY segment
ORDER BY revenue DESC;


-- Q17. Top 20 Customers by Revenue
SELECT
    customer_id,
    customer_name,
    segment,
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2)     AS total_spent,
    ROUND(AVG(sales), 2)     AS avg_order_value,
    MAX(order_date)          AS last_order_date
FROM retail_sales
GROUP BY customer_id, customer_name, segment, region
ORDER BY total_spent DESC
LIMIT 20;


-- Q18. RFM Scores in SQL
WITH snapshot AS (
    SELECT MAX(order_date) AS max_date FROM retail_sales
),
rfm_base AS (
    SELECT
        r.customer_id,
        r.customer_name,
        r.segment,
        DATEDIFF(s.max_date, MAX(r.order_date)) AS recency,
        COUNT(DISTINCT r.order_id)               AS frequency,
        ROUND(SUM(r.sales), 2)                   AS monetary
    FROM retail_sales r, snapshot s
    GROUP BY r.customer_id, r.customer_name, r.segment
),
percentiles AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency DESC)  AS r_score,
        NTILE(5) OVER (ORDER BY frequency)     AS f_score,
        NTILE(5) OVER (ORDER BY monetary)      AS m_score
    FROM rfm_base
)
SELECT
    customer_id,
    customer_name,
    segment,
    recency,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    r_score + f_score + m_score AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2                  THEN 'New Customers'
        WHEN r_score >= 3 AND m_score >= 3 AND f_score <= 2 THEN 'Potential Loyalists'
        WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost / Churned'
        WHEN r_score <= 2 AND m_score >= 3                  THEN 'Cant Lose Them'
        ELSE 'Needs Attention'
    END AS customer_segment
FROM percentiles
ORDER BY rfm_total DESC;


-- Q19. New vs Returning Customers per Year
WITH first_orders AS (
    SELECT customer_id, MIN(YEAR(order_date)) AS first_year
    FROM retail_sales
    GROUP BY customer_id
)
SELECT
    YEAR(rs.order_date) AS year,
    SUM(CASE WHEN YEAR(rs.order_date) = fo.first_year THEN 1 ELSE 0 END) AS new_customers,
    SUM(CASE WHEN YEAR(rs.order_date) > fo.first_year THEN 1 ELSE 0 END) AS returning_customers
FROM retail_sales rs
JOIN first_orders fo ON rs.customer_id = fo.customer_id
GROUP BY YEAR(rs.order_date)
ORDER BY year;


-- Q20. Average Days Between Orders (Repeat Customers)
WITH order_dates AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_order
    FROM (SELECT DISTINCT customer_id, order_date FROM retail_sales) t
)
SELECT
    customer_id,
    ROUND(AVG(DATEDIFF(order_date, prev_order)), 1) AS avg_days_between_orders
FROM order_dates
WHERE prev_order IS NOT NULL
GROUP BY customer_id
HAVING avg_days_between_orders IS NOT NULL
ORDER BY avg_days_between_orders ASC
LIMIT 20;


-- ═══════════════════════════════════════════════════════════
-- ── SECTION E: SHIPPING ANALYSIS ───────────────────────────
-- ═══════════════════════════════════════════════════════════

-- Q21. Revenue and Volume by Ship Mode
SELECT
    ship_mode,
    COUNT(*) AS transactions,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(AVG(DATEDIFF(ship_date, order_date)), 1) AS avg_ship_days
FROM retail_sales
GROUP BY ship_mode
ORDER BY revenue DESC;


-- Q22. Average Shipping Time by Region
SELECT
    region,
    ship_mode,
    ROUND(AVG(DATEDIFF(ship_date, order_date)), 2) AS avg_ship_days,
    MIN(DATEDIFF(ship_date, order_date))           AS min_days,
    MAX(DATEDIFF(ship_date, order_date))           AS max_days
FROM retail_sales
GROUP BY region, ship_mode
ORDER BY region, avg_ship_days;


-- ═══════════════════════════════════════════════════════════
-- ── SECTION F: BUSINESS RECOMMENDATIONS QUERIES ────────────
-- ═══════════════════════════════════════════════════════════

-- Q23. High Value Orders (> $1000)
SELECT
    order_id,
    customer_name,
    segment,
    region,
    category,
    product_name,
    ROUND(sales, 2) AS sales
FROM retail_sales
WHERE sales > 1000
ORDER BY sales DESC
LIMIT 30;


-- Q24. Low Value Orders that Are Frequent (possible discount abuse)
SELECT
    customer_id,
    customer_name,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(AVG(sales), 2) AS avg_order_value,
    ROUND(SUM(sales), 2) AS total_sales
FROM retail_sales
GROUP BY customer_id, customer_name
HAVING avg_order_value < 50 AND orders >= 5
ORDER BY orders DESC;


-- Q25. Category Performance Month over Month (Last Year)
SELECT
    category,
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(sales), 2) AS monthly_revenue
FROM retail_sales
WHERE YEAR(order_date) = (SELECT MAX(YEAR(order_date)) FROM retail_sales)
GROUP BY category, DATE_FORMAT(order_date, '%Y-%m')
ORDER BY category, month;


-- ═══════════════════════════════════════════════════════════
-- ── SECTION G: VIEWS FOR POWER BI ──────────────────────────
-- ═══════════════════════════════════════════════════════════

-- These views can be connected directly to Power BI

CREATE OR REPLACE VIEW vw_sales_kpis AS
SELECT
    COUNT(DISTINCT order_id)    AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2)        AS total_revenue,
    ROUND(AVG(sales), 2)        AS avg_order_value
FROM retail_sales;


CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    YEAR(order_date)             AS year,
    MONTH(order_date)            AS month,
    DATE_FORMAT(order_date, '%b %Y') AS period,
    ROUND(SUM(sales), 2)         AS revenue,
    COUNT(DISTINCT order_id)     AS orders,
    COUNT(DISTINCT customer_id)  AS customers
FROM retail_sales
GROUP BY YEAR(order_date), MONTH(order_date);


CREATE OR REPLACE VIEW vw_regional_summary AS
SELECT
    region,
    state,
    category,
    sub_category,
    segment,
    ship_mode,
    ROUND(SUM(sales), 2)        AS revenue,
    COUNT(DISTINCT order_id)    AS orders,
    COUNT(DISTINCT customer_id) AS customers
FROM retail_sales
GROUP BY region, state, category, sub_category, segment, ship_mode;


CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT
    customer_id,
    customer_name,
    segment,
    region,
    state,
    COUNT(DISTINCT order_id)                               AS orders,
    ROUND(SUM(sales), 2)                                   AS total_spent,
    ROUND(AVG(sales), 2)                                   AS avg_order_value,
    DATEDIFF(
        (SELECT MAX(order_date) FROM retail_sales),
        MAX(order_date)
    )                                                      AS days_since_last_order,
    MIN(order_date)                                        AS first_order,
    MAX(order_date)                                        AS last_order
FROM retail_sales
GROUP BY customer_id, customer_name, segment, region, state;
