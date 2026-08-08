"""
This sample module contains features logic that can be used to generate and populate tables in Feature Store. 
You should plug in your own features computation logic in the compute_features_fn method below.
"""
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType, FloatType, LongType


def _filter_df_by_ts(df, ts_column, start_date, end_date):
    if ts_column and start_date:
        df = df.filter(F.col(ts_column) >= start_date)
    if ts_column and end_date:
        df = df.filter(F.col(ts_column) < end_date)
    return df


def compute_features_fn(input_df, timestamp_column, start_date, end_date):
    """Contains logic to compute features.

    Given an input dataframe and time ranges, this function should compute features, populate an output dataframe and
    return it. This method will be called from a  Feature Store pipeline job and the output dataframe will be written
    to a Feature Store table. You should update this method with your own feature computation logic.

    The timestamp_column, start_date, end_date args are optional but strongly recommended for time-series based
    features.

    :param input_df: Input dataframe.
    :param timestamp_column: Column containing the timestamp. This column is used to limit the range of feature
    computation. It is also used as the timestamp key column when populating the feature table, so it needs to be
    returned in the output.
    :param start_date: Start date of the feature computation interval.
    :param end_date:  End date of the feature computation interval.
    :return: Output dataframe containing computed features given the input arguments.
    """
    df = _filter_df_by_ts(input_df, timestamp_column, start_date, end_date)

    population_features = (
       df.select(
        F.col("year").alias("year").cast(IntegerType()),
        F.col("yearly_change_pct").cast(FloatType()),
        F.col("yearly_change").cast(LongType()),
        F.coalesce(F.col("migrants").cast(LongType()), F.lit(0)).alias("migrants"),
        F.col("age_median").alias("age_median").cast(FloatType()),
        F.col("fertility_rate").alias("fertility_rate").cast(FloatType()),
        F.col("density").alias("density").cast(LongType()),
        F.col("pop_urban_pct").alias("pop_urban_pct").cast(FloatType()),
        F.col("pop_urban").alias("pop_urban").cast(LongType()),
        F.col("share_world").alias("share_world").cast(FloatType()),
        F.col("pop_world").alias("pop_world").cast(LongType()),
        F.col("rank_world").alias("rank_world").cast(IntegerType()),
       )
    )   
   
    return population_features
