// db.js

// Product CRUD (via Flask API)
async function getAllProducts() {
  const response = await fetch('/api/products');
  return await response.json();
}

async function addProduct(product) {
  await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(product)
  });
}

async function updateProduct(product) {
  const response = await getAllProducts();
  const existing = response.find(p => p.name === product.name);
  if (existing) {
    await fetch(`/api/products/${existing.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product)
    });
  }
}

async function deleteProduct(name) {
  const response = await getAllProducts();
  const product = response.find(p => p.name === name);
  if (product) {
    await fetch(`/api/products/${product.id}`, {
      method: 'DELETE'
    });
  }
}

// Order CRUD (via Flask API)
async function getAllOrders() {
  const response = await fetch('/api/orders');
  return await response.json();
}

async function addOrder(order) {
  await fetch('/api/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(order)
  });
}

async function updateOrderStatus(orderId, updatedOrder) {
  await fetch(`/api/orders/${orderId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updatedOrder)
  });
}


