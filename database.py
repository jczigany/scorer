from PySide2.QtSql import QSqlQuery

def create_tables(db):
    query = QSqlQuery("CREATE TABLE IF NOT EXISTS 'players' ('player_id'	INTEGER,'player_name'	TEXT,PRIMARY KEY('player_id' AUTOINCREMENT))", db=db)
    query.exec_()
    query = QSqlQuery("CREATE TABLE IF NOT EXISTS 'matches' ('match_id'	INTEGER,'leg_id'	INTEGER,'set_id'	INTEGER,'winner_id'	INTEGER,'timestamp'	TEXT)", db=db)
    query.exec_()
    query = QSqlQuery("CREATE TABLE IF NOT EXISTS 'dobas' ('player_id'	INTEGER,'round_number'	INTEGER,'points'	INTEGER,'leg_id'	INTEGER,'set_id'	INTEGER,'match_id'	INTEGER,'timestamp'	TEXT)", db=db)
    query.exec_()
    query = QSqlQuery("CREATE TABLE IF NOT EXISTS 'match_settings' ('match_id'	INTEGER,'player1_id'	INTEGER,'player2_id'	INTEGER,'variant'	TEXT,'sets'	INTEGER,'legsperset'	INTEGER,'timestamp'	INTEGER,PRIMARY KEY('match_id' AUTOINCREMENT))", db=db)
    query.exec_()
    query = QSqlQuery("INSERT INTO 'players' VALUES (1, 'Player 1')", db=db)
    query.exec_()
    query = QSqlQuery("INSERT INTO 'players' VALUES (2, 'Player 2')", db=db)
    query.exec_()