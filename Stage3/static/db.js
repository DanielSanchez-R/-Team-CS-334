// db.js

const DB_NAME = 'TeaShopDB';
const DB_VERSION = 1;
let db;

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = function (e) {
      db = e.target.result;

      if (!db.objectStoreNames.contains('products')) {
        const productStore = db.createObjectStore('products', { keyPath: 'name' });
        productStore.transaction.oncomplete = () => {
          console.log('Product store created');
        };
      }

      if (!db.objectStoreNames.contains('orders')) {
        db.createObjectStore('orders', { autoIncrement: true });
      }
    };

    request.onsuccess = function (e) {
      db = e.target.result;
      resolve(db);
    };

    request.onerror = function (e) {
      reject('Database error: ' + e.target.errorCode);
    };
  });
}

// Product CRUD
async function getAllProducts() {
  await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('products', 'readonly');
    const store = tx.objectStore('products');
    const request = store.getAll();
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject('Failed to get products');
  });
}

async function addProduct(product) {
  await openDB();
  const tx = db.transaction('products', 'readwrite');
  tx.objectStore('products').add(product);
}

async function updateProduct(product) {
  await openDB();
  const tx = db.transaction('products', 'readwrite');
  tx.objectStore('products').put(product);
}

async function deleteProduct(name) {
  await openDB();
  const tx = db.transaction('products', 'readwrite');
  tx.objectStore('products').delete(name);
}

// Order CRUD
async function getAllOrders() {
  await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('orders', 'readonly');
    const store = tx.objectStore('orders');
    const request = store.getAll();
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject('Failed to get orders');
  });
}

async function addOrder(order) {
  await openDB();
  const tx = db.transaction('orders', 'readwrite');
  tx.objectStore('orders').add(order);
}

async function updateOrderStatus(orderId, updatedOrder) {
  await openDB();
  const tx = db.transaction('orders', 'readwrite');
  tx.objectStore('orders').put(updatedOrder, orderId);
}

// Optional: one-time seeding from JSON if store is empty
async function seedProductsIfEmpty() {
  const existing = await getAllProducts();
  if (existing.length === 0) {
    const seedData = [
      { name: "New Mexico Green Tea", price: 5.99, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Black Tea", price: 6.99, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Peppermint Tea", price: 7.49, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Chamomile Tea", price: 5.49, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Hibiscus Tea", price: 6.79, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Mint Tea", price: 5.89, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Chai Tea", price: 7.99, image: "../static/assets/tea_background.png" },
      { name: "New Mexico White Tea", price: 8.49, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Oolong Tea", price: 9.49, image: "../static/assets/tea_background.png" },
      { name: "New Mexico Cinnamon Buns", price: 4.99, image: "../static/assets/tea_background.png" }
    ];
    for (const product of seedData) {
      await addProduct(product);
    }
    console.log('Seeded products into IndexedDB');
  }
}

// Run seed at startup
seedProductsIfEmpty();

