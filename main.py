from logs_splitter import Logs, Time

if __name__ == "__main__":
    filepath = "./log_to_split.log" # File with logs
    container_names = ["nginx-1", "shortener-1", "redis-1"] # Container names to filter, if not specified, it prints unspecified container names

    lines = Logs(filepath, container_names)
    # lines.split_logs_to_files_and_save() # Splits logs into files and sale

    from_time = Time(day=30, hour=3) # By default this year, this month and this day
    to_time = Time(day=30)

    lines.filter_logs_to_files_and_save(from_time, to_time) # Split and filter, and then save
