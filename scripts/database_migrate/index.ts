import 'zx/globals'
import { Knex, knex } from 'knex'

const EXAMPLE_JSON = {
  qq: 123456789,
  length: 23.34,
  register_time: '2023-01-25 02:26:52',
  daily_lock_count: 6,
  daily_pk_count: 6,
  daily_glue_count: 6,
  latest_daily_lock: '2023-01-25 02:26:52',
  latest_daily_pk: '2023-01-25 01:00:00',
  latest_daily_glue: '2023-01-25 02:26:52',
  pk_time: '2000-01-01 00:00:00',
  pked_time: '2020-01-01 00:00:01',
  glueing_time: '2023-01-25 02:26:52',
  glued_time: '2023-01-25 02:26:52',
  locked_time: '2023-01-25 02:26:52',
}

const USER_INFO_TABLE = {
  qq: 123456789,
  latest_speech_nickname: '',
  latest_speech_group: 987654321,
}

const run = async () => {
  const DATABASE_PATH = path.join(__dirname, './data.sqlite')
  const SQL_FILE = path.join(__dirname, './data_migrate.sql')
  const config: Knex.Config = {
    client: 'better-sqlite3',
    connection: {
      filename: DATABASE_PATH,
    },
  }
  const ins = knex(config)
  const sql: string[] = []

  try {
    // Create a table if not exists
    const createSql = await ins.schema
      .createTableIfNotExists('users', (table) => {
        // create primary key, name is qq
        table.bigint('qq').primary()
        table.float('length')
        ;['daily_lock_count', 'daily_pk_count', 'daily_glue_count'].forEach(
          (key) => {
            table.integer(key)
          }
        )
        ;[
          'register_time',
          'latest_daily_lock',
          'latest_daily_pk',
          'latest_daily_glue',
          'pk_time',
          'pked_time',
          'glueing_time',
          'glued_time',
          'locked_time',
        ].forEach((key) => {
          table.string(key)
        })
      })
      .toSQL()
    // @ts-expect-error
    sql.push(createSql[0].sql)
    // Insert data
    const insertSql = await ins('users').insert(EXAMPLE_JSON).toSQL()
    sql.push(insertSql.sql)
    // select single data by qq
    const selectSql = await ins('users')
      .select('*')
      .where('qq', 123456789)
      .toSQL()
    sql.push(selectSql.sql)
    // update single data by qq
    const updateSql = await ins('users')
      .update(EXAMPLE_JSON)
      .where('qq', 123456789)
      .toSQL()
    sql.push(updateSql.sql)
    // get all data counts
    const countSql = await ins.table('users').count().toSQL()
    sql.push(countSql.sql)
    // sort by length max 10
    const sortSql = await ins('users')
      .select('*')
      .orderBy('length', 'desc')
      .limit(10)
      .toSQL()
    sql.push(sortSql.sql)

    sql.push('-- User Info Table --')
    const createSqlWithUserInfo = await ins.schema
      .createTableIfNotExists('info', (table) => {
        table.bigint('qq').primary()
        table.string('latest_speech_nickname')
        table.bigint('latest_speech_group')
      })
      .toSQL()
    // @ts-expect-error
    sql.push(createSqlWithUserInfo[0].sql)
    const insertSqlWithUserInfo = await ins('info')
      .insert(USER_INFO_TABLE)
      .toSQL()
    sql.push(insertSqlWithUserInfo.sql)
    const selectSqlWithUserInfo = await ins('info')
      .select('*')
      .where('qq', 123456789)
      .toSQL()
    sql.push(selectSqlWithUserInfo.sql)
    // delete
    const deleteSqlWithUserInfo = await ins('info')
      .where('qq', 123456789)
      .del()
      .toSQL()
    sql.push(deleteSqlWithUserInfo.sql)

    sql.push('-- Rebirth Table --')
    const createSqlWithRebirth = await ins.schema
      .createTableIfNotExists('rebirth', (table) => {
        table.bigint('qq').primary()
        table.string('latest_rebirth_time')
        table.integer('level')
      })
      .toSQL()
    // @ts-expect-error
    sql.push(createSqlWithRebirth[0].sql)
    const insertSqlWithRebirth = await ins('rebirth')
      .insert({
        qq: 123456789,
        latest_rebirth_time: '2023-01-25 02:26:52',
        level: 1,
      })
      .toSQL()
    sql.push(insertSqlWithRebirth.sql)
    const selectSqlWithRebirth = await ins('rebirth')
      .select('*')
      .where('qq', 123456789)
      .toSQL()
    sql.push(selectSqlWithRebirth.sql)
    // delete
    const deleteSqlWithRebirth = await ins('rebirth')
      .where('qq', 123456789)
      .del()
      .toSQL()
    sql.push(deleteSqlWithRebirth.sql)

    // write
    fs.writeFileSync(SQL_FILE, sql.join(';\n') + ';\n', 'utf-8')
  } catch (e) {
    console.error(e)
  } finally {
    await ins.destroy()
  }
}

run()
