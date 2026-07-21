def winsorize(series):

    p10=series.quantile(.10)
    p90=series.quantile(.90)

    return series.clip(p10,p90)


def normalize(series):

    return (
        (series-series.min())
        /
        (series.max()-series.min())
        *100
    )

