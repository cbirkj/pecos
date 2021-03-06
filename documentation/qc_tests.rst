Quality control tests
======================

Pecos includes several quality control tests.
When a test fails, information is stored in a summary table.  This
information can be saved to a file, database, or included in reports.
Quality controls tests fall into five categories:

* Timestamp
* Missing data
* Corrupt data
* Range
* Increment

Timestamp test
--------------------
The :class:`~pecos.monitoring.PerformanceMonitoring.check_timestamp` method is used to check the time index for missing, 
duplicate, and non-monotonic indexes.  If a duplicate timestamp is found, Pecos keeps the first occurrence.  
If timestamps are not monotonic, the timestamps are reordered.
For this reason, the timestamp should be corrected before other quality control 
tests are run.
Input includes:

* Expected frequency of the time series in seconds

* Minimum number of consecutive failures for reporting (default = 1 timestamp)

* A flag indicating if exact timestamps are expected.  When set to False, irregular timestamps can be used in the Pecos analysis.

For example::

	pm.check_timestamp(60)

checks for missing, duplicate, and non-monotonic indexes assuming an expected 
frequency of 60 seconds.
	
Missing data test
--------------------
The :class:`~pecos.monitoring.PerformanceMonitoring.check_missing` method is used to check for missing values.  
Unlike missing timestamps, missing data only impacts a subset of data columns.
NaN is included as missing.
Input includes:

* Data column (default = all columns)

* Minimum number of consecutive failures for reporting (default = 1 timestamp)

For example::

	pm.check_missing('Wave', min_failures=5)

checks for missing data in the columns associated with the key 'Wave'.  In this case, warnings 
are only reported if there are 5 consecutive failures.

Corrupt data test
--------------------
The :class:`~pecos.monitoring.PerformanceMonitoring.check_corrupt` method is used to check for corrupt values. 
Input includes:

* List of corrupt values

* Data column (default = all columns)

* Minimum number of consecutive failures for reporting (default = 1 timestamp)

For example::

	pm.check_corrupt([-999, 999])

checks for data with values -999 or 999 in the entire DataFrame.

Range test
--------------------
The :class:`~pecos.monitoring.PerformanceMonitoring.check_range` method is used to check that data is within an expected range.
Range tests are very flexible.  The test can be used to check for expected range on modeled
vs. measured values (i.e. absolute error or relative error) or an expected
relationships between data columns (i.e. column A divided by column B). 
An upper bound, lower bound or both can be specified.  
Additionally, the data can be smoothed using a rolling mean.
Input includes:

* Upper and lower bound

* Data column (default = all columns)

* Rolling mean window (default = 1 timestamp, which indicates no rolling mean)

* Minimum number of consecutive failures for reporting (default = 1 timestamp)

For example::

	pm.check_range([None,1], 'A', rolling_window=2)

checks for values greater than 1 in the columns associated with the key 'A', 
using a rolling average of 2 time steps.

Increment test
--------------------
The :class:`~pecos.monitoring.PerformanceMonitoring.check_increment` method is used to check that the difference between 
consecutive data values (or other specified increment) is within an expected range.
This method can be used to test if data is not changing or if the data has an 
abrupt change.  Like the check_range method, the user can specify if the data
should be smoothed using a rolling mean.  
Input includes:

* Upper and lower bound

* Data column (default = all columns)

* Increment used for difference calculation (default = 1 timestamp)

* Flag indicating if the absolute value is taken (default = True)

* Rolling mean window (default = 1 timestamp, which indicates no rolling mean)

* Minimum number of consecutive failures for reporting (default = 1 timestamp)

For example::

	pm.check_increment([None, 0.000001], min_failure=60)

checks if value increments are greater than 0.000001 for 60 consecutive time steps::

	pm.check_increment([-800, None], absolute_value = False)

checks if value increments decrease by more than -800 in a single time step.

