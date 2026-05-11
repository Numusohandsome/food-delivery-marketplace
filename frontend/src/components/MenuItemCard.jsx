function MenuItemCard({ item, onAddToCart }) {
  return (
    <article className="menu-item-card">
      <div>
        <h3>{item.name}</h3>
        <p>{item.description}</p>
        <strong>${Number(item.price).toFixed(2)}</strong>
      </div>

      <button onClick={() => onAddToCart(item)}>Add to cart</button>
    </article>
  );
}

export default MenuItemCard;