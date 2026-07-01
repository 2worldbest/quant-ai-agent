def calculate_moving_average(close_prices, window=20):
    """
    종가 데이터를 이용해 이동평균선을 계산한다.
    기본값은 20일선이다.
    """

    return close_prices.rolling(window=window).mean()