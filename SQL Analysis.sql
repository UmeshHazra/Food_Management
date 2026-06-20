use food;

select count(*) from claims_data;

drop table receivers_data;

select * from food_listings_data;
select * from claims_data;
select * from clean_providers_data;
select * from clean_receivers_data;

alter table clean_receivers_data
add constraint PK_Receivers
primary key (Receiver_ID);

alter table food_listings_data
add constraint PK_Food_Listings
primary key (Food_ID);

# 1. Total Providers in Each City
select City, count(*) as Total_Providers
from clean_providers_data
group by City
order by Total_Providers desc;

# 2. Total Receivers in Each City
select City , count(*) as Total_Receivers
from clean_receivers_data
group by City
order by Total_Receivers desc;

# 3. Provider Type Contributing Most Food
select Provider_Type,
sum(Quantity) as Total_Quantity
from food_listings_data
group by Provider_Type
order by Total_Quantity desc;

# 4. Contact Details of Providers in a Specific City
SELECT Name, Contact, Address
FROM clean_providers_data
WHERE City = 'New Jessica';

# 5. Total Quantity of Available Food
select sum(Quantity) as Total_Quantity
from food_listings_data;

# 6. City with Highest Food Listings
select Location,
count(*) as Food_Count
from food_listings_data
group by Location
order by Food_Count desc
limit 1;

# 7. Most Common Food Type
select Food_Type,
count(*) as Frequency
from food_listings_data
group by Food_Type
order by Frequency desc;

# 8. Claims Made for Each Food Item
SELECT f.Food_Name,
       COUNT(c.Claim_ID) AS Total_Claims
FROM food_listings_data f
LEFT JOIN claims_data c
ON f.Food_ID = c.Food_ID
GROUP BY f.Food_Name
ORDER BY Total_Claims DESC;

# 9. Provider with Highest Successful Claims
select p.Name,
count(c.Claim_ID) as Sucessfull_Claim
from clean_providers_data p
join food_listings_data f
on p.Provider_ID = f.Provider_ID
join claims_data c
on f.Food_ID = c.Food_Id
where c.Status = "Completed"
group by p.Name
order by Sucessfull_Claim desc;

# 10. Claim Status Percentage
SELECT Status,
       ROUND(COUNT(*) * 100.0 /
       (SELECT COUNT(*) FROM claims_data),2)
       AS Percentage
FROM claims_data
GROUP BY Status;

# 11. Average Quantity Claimed Per Receiver
select r.Name,
avg(f.Quantity) as Avg
from clean_receivers_data r
join claims_data c
on c.Receiver_Id = r.Receiver_ID
join food_listings_data f
on c.Food_ID = f.Food_ID
group by r.Name;

# 12. Most Claimed Meal Type
select f.Meal_Type,
count(c.Claim_ID) as Claims
from food_listings_data f
join claims_data c
on c.Food_ID = f.Food_ID
group by f.Meal_Type
order by Claims desc;

# 13. Total Food Donated by Each Provider
SELECT p.Name,
       SUM(f.Quantity) AS Total_Donated
FROM clean_providers_data p
JOIN food_listings_data f
ON p.Provider_ID = f.Provider_ID
GROUP BY p.Name
ORDER BY Total_Donated DESC;

# 14. Top 5 Receivers
SELECT r.Name,
       COUNT(c.Claim_ID) AS Total_Claims
FROM clean_receivers_data r
JOIN claims_data c
ON r.Receiver_ID = c.Receiver_ID
GROUP BY r.Name
ORDER BY Total_Claims DESC
LIMIT 5;

# 15. Food Items Expiring Today
select Food_Name,
Quantity,
Expiry_Date
from food_listings_data
where Expiry_Date = curdate();

# 16. Food Items Expiring Within 2 Days
select Food_Name,
Quantity,
Expiry_Date
from food_listings_data
where Expiry_Date <= date_add(curdate(), interval 2 day);

# 17. Unclaimed Food Items
select f.Food_Name
from food_listings_data f
join claims_data c
on c.Food_ID = f.Food_ID
where c.Claim_ID is null;

# 18. City with Highest Food Demand
select r.City,
count(c.Claim_ID) as Demand
from clean_receivers_data r
join claims_data c
on c.Receiver_ID = r.Receiver_ID
group by r.City
order by Demand desc;

# 19. Monthly Claim Trend
SELECT MONTH(Timestamp) AS Month_No,
       COUNT(*) AS Claims
FROM claims_data
GROUP BY MONTH(Timestamp)
ORDER BY Month_No;

# 20. Food Wastage Risk Analysis
SELECT Food_Type,
       COUNT(*) AS Near_Expiry_Items
FROM food_listings_data
WHERE Expiry_Date <= DATE_ADD(CURDATE(), INTERVAL 2 DAY)
GROUP BY Food_Type
ORDER BY Near_Expiry_Items DESC;