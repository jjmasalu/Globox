# A/B Test Report: Food and Drink Banner

## Purpose
Evaluate the impact of a redesigned homepage with banner (B) compared to the existing one with no banner (A) on average spending and conversion rates.


## Hypotheses
- Null hypothesis: H0 = There is no difference in the conversion rates btn the control and treatment groups r0 = r1   
- Alternative hypothesis: H1 =  conversion rates are different btn the groups (r0 != r1)


- Null Hypothesis H0: There is no difference in average spending per user btn the two groups
- Alternative Hypothesis H1: There is a difference ein average spending per user btn the two groups.


## Methodology
### Test Design
- **Population:** 
  - Control group = 24343 users  
  - Treatment group =  24600
- **Duration:** Test start and end dates.
- **Success Metrics:** 
  - Conversion rate
  - Average spending
## Results
### Data Analysis
- **Pre-Processing Steps:**
  - Null Values were replaced by 'other' in text fields and 0 in numerical fields
```sql

WITH globox_activity AS(
    SELECT users.id,
           COALESCE(users.country, 'other') AS country,
           COALESCE(users.gender, 'O') AS gender,
           COALESCE(SUM(activity.spent), 0) AS spent,
           COALESCE(groups.device, 'other') AS device,
           CASE
               WHEN groups.group = 'A' THEN 'Control'
               WHEN groups.group = 'B' THEN 'Treatment'
               ELSE 'not assigned'
           END AS group_kind,
           CASE
               WHEN COALESCE(SUM(activity.spent), 0) > 0 THEN 1
   			   WHEN COALESCE(SUM(activity.spent), 0) <=0 THEN 0
           END AS converted
  
    FROM users
    LEFT JOIN activity ON users.id = activity.uid
    LEFT JOIN groups ON users.id = groups.uid
    GROUP BY users.id,
             groups.device,
    				 groups.group
    
    )
    
SELECT *
FROM globox_activity
;



```

- **Statistical Tests Used:** 
   - Z_test was used for the difference in proportions
   - t_ test was used for te difference in mean
- **Results Overview:** 
  
### Findings
**Analyzing Difference in proportions between the Two groups**
  - The value of the test statistic was:  3.864291770414927
  - The p value was:  0.00011141198532947085
  - The sample statistic is :  0.0070698225796701555
  

**Analyzing Difference in mean between the Two groups**
  - The value of the test statistic was:  0.07042491002232414
  - The p value was:  0.9438557531531295
  

## Interpretation
- **Outcome of the Test(s):**
    - Since the p_value(0.943..) for the difference in mean is greater than 0.05, it is statistically insignificant,
      therefore we fail to reject the null hypothesis that "there was no difference in the average user spending btn the two groups"
    - Since the p_value(0.0001...) for the difference in proportions  is less than 0.05, we reject the null hypothesis,
      that the treatment group and control group have no difference in their conversion rates
- **Confidence Level:** (95%)
    - confidence interval for the difference in mean:  (-0.4386612811146449, 0.4713582370400918)
    - confidence interval for the difference in proportion: (0.0034860511629807105, 0.0106535939963596)


## Conclusions
- **Key Takeaways:** The banner will increase the revenue of the company though not by much
- **Limitations/Considerations:** The fact that the treatment group had an upper hand on the number of observations involved has been neglected, this could be a potential explanation as to why there is a small rise in conversion rate in this group.

## Recommendations
- **Next Steps:** Though small, but a significant rise in conversion rate and average spending has been observed in the treatment group, therefore the business should launch the banner to all it's customers.
- **Further Analysis:** We could try and take an equal number of samples for both groups and conduct the test over a longer duration of time to see the effects on a long run.

