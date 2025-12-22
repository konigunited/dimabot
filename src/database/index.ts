import Database from 'better-sqlite3';
import path from 'path';

// Создаем базу данных
const db = new Database(path.join(process.cwd(), 'orders.db'));

// Инициализация таблиц
export function initDatabase() {
  // Таблица пользователей
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY,
      username TEXT,
      first_name TEXT,
      last_name TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Таблица заказов
  db.exec(`
    CREATE TABLE IF NOT EXISTS orders (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      prompt_id TEXT NOT NULL,
      price INTEGER NOT NULL,
      status TEXT DEFAULT 'pending',
      payment_id TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
  `);

  // Миграция: добавление колонки payment_id если её нет
  try {
    db.exec(`
      ALTER TABLE orders ADD COLUMN payment_id TEXT
    `);
    console.log('✅ Миграция: добавлена колонка payment_id');
  } catch (error: any) {
    // Колонка уже существует, игнорируем ошибку
    if (!error.message.includes('duplicate column name')) {
      console.log('ℹ️  Колонка payment_id уже существует');
    }
  }

  // Миграция: добавление колонки updated_at если её нет
  try {
    db.exec(`
      ALTER TABLE orders ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    `);
    console.log('✅ Миграция: добавлена колонка updated_at');
  } catch (error: any) {
    // Колонка уже существует, игнорируем ошибку
    if (!error.message.includes('duplicate column name')) {
      console.log('ℹ️  Колонка updated_at уже существует');
    }
  }

  console.log('✅ База данных инициализирована');
}

// Сохранить или обновить пользователя
export function saveUser(userId: number, username?: string, firstName?: string, lastName?: string) {
  const stmt = db.prepare(`
    INSERT INTO users (user_id, username, first_name, last_name)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
      username = excluded.username,
      first_name = excluded.first_name,
      last_name = excluded.last_name
  `);

  stmt.run(userId, username, firstName, lastName);
}

// Создать заказ
export function createOrder(userId: number, promptId: string, price: number): number {
  const stmt = db.prepare(`
    INSERT INTO orders (user_id, prompt_id, price, status)
    VALUES (?, ?, ?, 'pending')
  `);

  const result = stmt.run(userId, promptId, price);
  return result.lastInsertRowid as number;
}

// Обновить статус заказа
export function updateOrderStatus(orderId: number, status: string, paymentId?: string) {
  const stmt = db.prepare(`
    UPDATE orders
    SET status = ?, payment_id = ?
    WHERE id = ?
  `);

  stmt.run(status, paymentId || null, orderId);
}

// Получить заказ по ID
export function getOrderById(orderId: number) {
  const stmt = db.prepare(`
    SELECT * FROM orders WHERE id = ?
  `);

  return stmt.get(orderId);
}

// Получить заказ по payment_id
export function getOrderByPaymentId(paymentId: string) {
  const stmt = db.prepare(`
    SELECT * FROM orders WHERE payment_id = ?
  `);

  return stmt.get(paymentId);
}

// Получить заказы пользователя
export function getUserOrders(userId: number) {
  const stmt = db.prepare(`
    SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC
  `);

  return stmt.all(userId);
}

// Проверить, покупал ли пользователь промпт
export function hasUserPurchased(userId: number, promptId: string): boolean {
  const stmt = db.prepare(`
    SELECT COUNT(*) as count FROM orders
    WHERE user_id = ? AND prompt_id = ? AND status = 'paid'
  `);

  const result = stmt.get(userId, promptId) as { count: number };
  return result.count > 0;
}

export { db };
