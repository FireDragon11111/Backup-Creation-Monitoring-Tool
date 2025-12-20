def monitor_directories(profile, tree):
    def safe_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    log_message(tree, f"Started Monitoring Directories for: {profile}")
    
    while monitoring_states.get(profile, False):
        config = load_config(profile)

        dest_dir = config.get('dest_dir', '')
        source_dir = config.get('source_dir', '')
        sub_dirs = config.get('sub_dirs', [])
        zip_files_kept = safe_int(config.get('zip_files_kept', 3), 3)
        interval_days = safe_int(config.get('interval_days', 0), 0)
        interval_hours = safe_int(config.get('interval_hours', 0), 0)
        interval_minutes = safe_int(config.get('interval_minutes', 0), 0)
        interval_seconds = safe_int(config.get('interval_seconds', 0), 0)
        interval = timedelta(days=interval_days, hours=interval_hours, minutes=interval_minutes, seconds=interval_seconds)
        if interval.total_seconds() <= 0:
            interval = timedelta(seconds=60)

        backup_frequency = config.get('backup_frequency', 'Daily')
        backup_time_str = config.get('backup_time', '')
        backup_day_of_week = config.get('backup_day_of_week', '')
        backup_day_of_month = config.get('backup_day_of_month', '')

        if backup_time_str:
            backup_time = datetime.strptime(backup_time_str, "%H:%M").time()
            now = datetime.now()
            backup_datetime = datetime.combine(now.date(), backup_time)
            window_end = backup_datetime + interval
            current_day_of_week = now.strftime("%A")
            current_day_of_month = now.day
            should_run = backup_datetime <= now < window_end

            if backup_frequency == 'Daily':
                if should_run:
                    if monitoring_states.get(profile, False):
                        if source_dir and dest_dir:
                            run_backup(source_dir, dest_dir, sub_dirs, tree, profile)
                        else:
                            log_message(tree, f"Error: Source or destination directory is empty for {profile}")

            elif backup_frequency == 'Weekly':
                if current_day_of_week == backup_day_of_week and should_run:
                    if monitoring_states.get(profile, False):
                        if source_dir and dest_dir:
                            run_backup(source_dir, dest_dir, sub_dirs, tree, profile)
                        else:
                            log_message(tree, f"Error: Source or destination directory is empty for {profile}")

            elif backup_frequency == 'Monthly':
                if isinstance(backup_day_of_month, str):
                    backup_day_of_month = safe_int(backup_day_of_month.split('/')[0], 1)
                else:
                    backup_day_of_month = safe_int(backup_day_of_month, 1)
                
                if current_day_of_month == backup_day_of_month and should_run:
                    if monitoring_states.get(profile, False):
                        if source_dir and dest_dir:
                            run_backup(source_dir, dest_dir, sub_dirs, tree, profile)
                        else:
                            log_message(tree, f"Error: Source or destination directory is empty for {profile}")
                    except Exception as e:
                        log_message(tree, f"Error: Failed to delete: {e}", old_file)

        time.sleep(interval.total_seconds())
