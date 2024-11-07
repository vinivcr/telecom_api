from datetime import datetime, timedelta


def calculate_call_duration(start_time, end_time):
    # Verifica se start_time e end_time são strings; se sim, converte para datetime
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

    # Calcula a duração
    duration = end_time - start_time

    # Formata a duração em HhMmSs
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h{int(minutes)}m{int(seconds)}s", duration.total_seconds(
    )


def calculate_call_price(start_time, end_time):
    # Verifica se start_time e end_time são strings; se sim, converte para datetime
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

    # Tarifas de preços
    fixed_rate = 0.36  # Taxa fixa para todas as chamadas
    standard_per_minute_rate = 0.09  # Tarifa por minuto no horário padrão

    # Define o total inicial com a taxa fixa
    total_price = fixed_rate

    # Itera minuto a minuto, considerando apenas minutos completos no horário padrão
    current_time = start_time
    while current_time + timedelta(seconds=59) < end_time:
        next_minute = current_time + timedelta(minutes=1)

        # Aplica o custo por minuto somente no horário padrão, até exatamente as 22:00
        if current_time.hour >= 6 and current_time.hour < 22:
            # Se o próximo minuto ultrapassa as 22:00, não cobra o minuto extra
            if next_minute.hour == 22 and next_minute.minute == 0:
                break
            total_price += standard_per_minute_rate

        # Avança para o próximo minuto
        current_time = next_minute

    # Retorna o preço final arredondado
    return round(total_price, 2)
