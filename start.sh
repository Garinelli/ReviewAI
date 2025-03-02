python -m src.bot.bot &
python -m src.bot.broker.bot_consumer &
python -m src.bot.broker.nn_consumer &
python -m src.bot.broker.parser_consumer &
python -m src.bot.broker.preprocessing_consumer &

wait