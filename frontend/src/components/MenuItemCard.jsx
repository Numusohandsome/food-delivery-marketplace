function MenuItemCard({ item, onAddToCart }) {
  return (
    <div className="menu-item-card">
      <div>
        <h3>{item.name}</h3>
        <p>{item.description}</p>
        <strong>${item.price.toFixed(2)}</strong>
      </div>

      <button onClick={() => onAddToCart(item)}>Add to cart</button>
    </div>
  );
}

export default MenuItemCard;