export default function ShopifyItem({ name, price, url, image }) {
    return (
        <a href={url} target="_blank" rel="noopener noreferrer" className="block w-64 h-80 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 ease-in-out mb-6 bg-gradient-to-r from-[#25292E] to-[#40464e] animate-gradient-x">
            <img className="w-full h-48 object-cover" src={image} alt={name} />
            <div className="flex items-center justify-between px-6 py-4">
                <div>
                    <div className="font-bold text-xl mb-2 text-white">{name}</div>
                    <p className="text-white text-base">${price}</p>
                </div>
                <img src="shopify.png" alt="Shopify logo" className="h-12 w-auto" />
            </div>
        </a>
    );
}