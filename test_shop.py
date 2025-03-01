"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart

PRICE_BOOK = 99.99
QUANTITY_BOOK = 987
PRICE_NEWSPAPER = 0.73
PRICE_MAGAZINE = 1.01
QUANTITY_NEWSPAPER = 123
DEFAULT_BUY_COUNT = 17


@pytest.fixture
def product_book() -> Product:
    return Product("book", PRICE_BOOK, "This is a book", QUANTITY_BOOK)


@pytest.fixture
def product_newspaper() -> Product:
    return Product("newspaper", PRICE_NEWSPAPER, "This is a newspaper", QUANTITY_NEWSPAPER)


@pytest.fixture
def product_magazine() -> Product:
    return Product("magazine", PRICE_MAGAZINE, "This is a magazine", QUANTITY_NEWSPAPER)


@pytest.fixture
def empty_cart() -> Cart:
    return Cart()


@pytest.fixture
def cart_with_products(product_book, product_newspaper) -> Cart:
    cart = Cart()
    cart.add_product(product_book, DEFAULT_BUY_COUNT)
    cart.add_product(product_newspaper, DEFAULT_BUY_COUNT)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize("quantities", [-1, 0, QUANTITY_BOOK - 1, QUANTITY_BOOK])
    def test_product_check_quantity(self, product_book, quantities):
        # TODO напишите проверки на метод check_quantity
        assert product_book.check_quantity(quantities)

    def test_product_check_quantity_more_than_available(self, product_book):
        assert not product_book.check_quantity(QUANTITY_BOOK + 1)

    @pytest.mark.parametrize("quantities", [1, QUANTITY_BOOK - 1, QUANTITY_BOOK])
    def test_product_buy(self, product_book, quantities):
        # TODO напишите проверки на метод buy

        expected = product_book.quantity - quantities
        product_book.buy(quantities)
        actual = product_book.quantity
        assert actual == expected

    def test_product_buy_more_than_available(self, product_book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        with pytest.raises(ValueError):
            product_book.buy(QUANTITY_BOOK + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    @pytest.mark.parametrize("cart_fixture, quantities, expected_quantities",
                             [("empty_cart", DEFAULT_BUY_COUNT, DEFAULT_BUY_COUNT),
                              ("empty_cart", 1, 1),
                              ("cart_with_products", 1, DEFAULT_BUY_COUNT + 1),
                              ("cart_with_products", 0, DEFAULT_BUY_COUNT),
                              ("cart_with_products", -1, DEFAULT_BUY_COUNT),
                              ("cart_with_products", None, DEFAULT_BUY_COUNT)])
    def test_add_product_cart(self, request, cart_fixture, quantities, expected_quantities, product_book):
        cart = request.getfixturevalue(cart_fixture)
        cart.add_product(product_book, quantities)
        assert product_book in cart.products
        assert cart.products[product_book] == expected_quantities

    @pytest.mark.parametrize("cart_fixture, expected_quantities", [("empty_cart", 1),
                                                                   ("cart_with_products", DEFAULT_BUY_COUNT + 1)])
    def test_add_product_cart_without_param_buy_count(self, request, cart_fixture, expected_quantities, product_book):
        cart = request.getfixturevalue(cart_fixture)
        cart.add_product(product_book)
        assert cart.products[product_book] == expected_quantities

    def test_remove_partition_product_cart(self, cart_with_products, product_book, product_newspaper):
        cart_with_products.remove_product(product_book, 5)
        assert cart_with_products.products[product_book] == DEFAULT_BUY_COUNT - 5

    @pytest.mark.parametrize("product_fixture, quantities", [("product_book", None),
                                                             ("product_newspaper", DEFAULT_BUY_COUNT),
                                                             ("product_book", DEFAULT_BUY_COUNT + 1)])
    def test_remove_full_product_cart(self, request, product_fixture, quantities, cart_with_products):
        product = request.getfixturevalue(product_fixture)
        cart_with_products.remove_product(product, quantities)
        assert product not in cart_with_products.products

    def test_remove_product_without_param_remove_count(self, cart_with_products, product_book, product_newspaper):
        cart_with_products.remove_product(product_book)
        assert product_book not in cart_with_products.products
        assert product_newspaper in cart_with_products.products

    def test_remove_product_not_in_cart(self, empty_cart, cart_with_products, product_book, product_newspaper,
                                        product_magazine):
        empty_cart.remove_product(product_book)
        assert product_book not in empty_cart.products

        cart_with_products.remove_product(product_magazine)
        assert product_magazine not in cart_with_products.products
        assert product_book in cart_with_products.products
        assert cart_with_products.products[product_book] == DEFAULT_BUY_COUNT
        assert product_newspaper in cart_with_products.products
        assert cart_with_products.products[product_newspaper] == DEFAULT_BUY_COUNT

    @pytest.mark.parametrize("cart_fixture", ["empty_cart", "cart_with_products"])
    def test_clear_cart(self, request, cart_fixture):
        cart = request.getfixturevalue(cart_fixture)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price_cart(self, empty_cart, cart_with_products):
        assert empty_cart.get_total_price() == 0.0
        assert isinstance(cart_with_products.get_total_price(), float)
        assert cart_with_products.get_total_price() == round(DEFAULT_BUY_COUNT * (PRICE_BOOK + PRICE_NEWSPAPER), 2)

    def test_buy_cart(self, cart_with_products, product_book, product_newspaper):
        cart_with_products.buy()
        assert product_book.quantity == QUANTITY_BOOK - DEFAULT_BUY_COUNT
        assert product_newspaper.quantity == QUANTITY_NEWSPAPER - DEFAULT_BUY_COUNT
        assert len(cart_with_products.products) == 0

    def test_buy_cart_rase_value_error(self, empty_cart, product_newspaper):
        empty_cart.add_product(product_newspaper, QUANTITY_NEWSPAPER + 1)
        with pytest.raises(ValueError):
            empty_cart.buy()
