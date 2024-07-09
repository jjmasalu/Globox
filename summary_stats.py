import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import norm, ttest_ind, t
import seaborn as sns

globox_data = pd.read_csv('globox_activity.csv')
alpha = 0.05

print('\nANALYZING THE DIFFERENCE IN PROPORTIONS BETWEEN THE TWO GROUPS\n')
print('Hypothesis Testing for the difference in proportions:\n ')
print('Null hypothesis: H0 = There is no difference in the conversion rates btn the control and treatment groups r0 = '
      'r1')
print('Alternative hypothesis: H1 =  conversion rates are different btn the groups (r0 != r1)\n')

count_converted_by_group = globox_data.pivot_table(values='converted', index='group_kind', aggfunc='sum')
count_totals_by_group = globox_data.pivot_table(values='id', index='group_kind', aggfunc=np.count_nonzero)

# count of those who converted in the control group and treatment group
count_control_converted = count_converted_by_group['converted']['Control']
count_treatment_converted = count_converted_by_group['converted']['Treatment']

# total count of members in the control and treatment group
count_control = count_totals_by_group['id']['Control']
count_treatment = count_totals_by_group['id']['Treatment']

counts = np.array([count_treatment_converted, count_control_converted])
nobs = np.array([count_treatment, count_control])
alternative = 'two-sided'  # the alternative hypothesis

z_stat, p_val = proportions_ztest(counts, nobs, alternative=alternative)
print('The value of the test statistic is: ', z_stat)
print('The p value is : ', p_val)

print('Since the p_value is less than 0.05, we reject the null hypothesis,\n'
      'that the treatment group and control group have no difference in their conversion rates\n')

# for confidence interval
print('Confidence interval of the difference in proportions:\n ')

# for sample statistic (difference in sample proportions)
proportion_control = count_control_converted/count_control
proportion_treatment = count_treatment_converted/count_treatment
sample_statistic = proportion_treatment - proportion_control  # difference in proportion
print('The sample statistic is : ', sample_statistic)

# for the critical value
critical_value = norm.ppf(1-alpha/2)

# for the standard error
standard_error = np.sqrt((proportion_treatment*(1-proportion_treatment)/count_treatment) + (
              proportion_control * (1 - proportion_control) / count_control))

# confidence interval

lower_bound = sample_statistic - critical_value*standard_error
upper_bound = sample_statistic + critical_value*standard_error
ci = (lower_bound, upper_bound)
print('confidence interval: ', ci)


print('\n\nANALYZING THE DIFFERENCE IN MEAN BETWEEN THE TWO GROUPS')

print('Hypothesis testing of the difference in average spending per user btn the two groups:\n')
print('''Null Hypothesis H0: There is no difference in average spending per user btn the two groups
Alternative Hypothesis H1: There is a difference ein average spending per user btn the two groups.\n''')
average_spending_by_group = globox_data.pivot_table(values='total_spending', index='group_kind')
control_group_data = globox_data[globox_data['group_kind'] == 'Control']
treatment_group_data = globox_data[globox_data['group_kind'] == 'Treatment']

# test statistic and p_value
t_statistic, p_value = ttest_ind(treatment_group_data["total_spending"], control_group_data['total_spending'], equal_var=False)
print('\nThe test statistic for the difference in mean is: ', t_statistic)
print('The p value for the difference in mean is: ', p_value)
print('\nConclusion: '
      'Since the p_value is greater than 0.05, it is statistically insignificant,\ntherefore we fail to reject the '
      'null hypothesis that "there was no difference in the average user spending btn the two groups"\n')


# Confidence interval of the difference in mean
print('Confidence interval for the difference in mean btn the two groups:\n')
# sample statistics
control_group_mean = np.mean(control_group_data['total_spending'])
treatment_group_mean = np.mean(treatment_group_data['total_spending'])
control_group_std = np.std(control_group_data['total_spending'], ddof=1)
treatment_group_std = np.std(treatment_group_data['total_spending'], ddof=1)

# standard error
standard_error = np.sqrt((control_group_std**2/len(control_group_data['total_spending'])) +
                         (treatment_group_std**2/len(treatment_group_data['total_spending'])))

confidence_level = 0.95
degrees_of_freedom = min(len(control_group_data['total_spending']) - 1 ,  len(treatment_group_data['total_spending']) - 1)
margin_of_error = t.ppf((1 + confidence_level) / 2, degrees_of_freedom) * standard_error

lower_bound = abs(control_group_mean - treatment_group_mean) - margin_of_error
upper_bound = abs(control_group_mean - treatment_group_mean) + margin_of_error
conf_interval = (lower_bound, upper_bound)
print('The confidence interval for the difference in mean btn the two groups is: ', conf_interval)

import matplotlib.pyplot as plt

# Visualizing Difference in Proportions
sns.barplot(x=['Treatment', 'Control'], y=[proportion_treatment, proportion_control])
plt.title('Conversion Rates in Treatment and Control Groups')
plt.xlabel('Group')
plt.ylabel('Conversion Rate')
plt.show()

# Visualizing Confidence Interval for the Difference in Means
sns.pointplot(x=['Treatment', 'Control'], y=[treatment_group_mean, control_group_mean], color='red')
plt.errorbar(x=['Treatment', 'Control'], y=[treatment_group_mean, control_group_mean],
             yerr=margin_of_error, fmt=' ', color='black')
plt.title('Difference in Mean Spending between Treatment and Control Groups')
plt.xlabel('Group')
plt.ylabel('Average Spending')
plt.show()

