"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart

PRICE_BOOK = 100
QUANTITY_BOOK = 1000
PRICE_NEWSPAPER = 10
QUANTITY_NEWSPAPER = 100
DEFAULT_BUY_COUNT = 10


@pytest.fixture
def product_book() -> Product:
    return Product("book", PRICE_BOOK, "This is a book", QUANTITY_BOOK)


@pytest.fixture
def product_newspaper()-> Product:
    return Product("newspaper", PRICE_NEWSPAPER, "This is a newspaper", QUANTITY_NEWSPAPER)


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
    @pytest.mark.parametrize("product_fixture, quantities, expected_pass", [("product_book", -1, True),
                                                                         ("product_book", 0, True),
                                                                         ("product_book", QUANTITY_BOOK - 1, True),
                                                                         ("product_book", QUANTITY_BOOK, True),
                                                                         ("product_book", QUANTITY_BOOK + 1, False)])
    def test_product_check_quantity(self, request, product_fixture, quantities, expected_pass):
        # TODO напишите проверки на метод check_quantity
        product = request.getfixturevalue(product_fixture)
        if expected_pass:
            assert product.check_quantity(quantities)
        else:
            assert not product.check_quantity(quantities)

    def test_product_buy(self, product_book):
        # TODO напишите проверки на метод buy

        expected = product_book.quantity - 1
        product_book.buy(1)
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

    @pytest.mark.parametrize("initial_quantities, add_quantities, expected_quantities", [(0, None, 1),
                                                                                    (0, 1, 1),
                                                                                    (1, None, 2),
                                                                                    (1, 2, 3), ])
    def test_add_product_cart(self, empty_cart, product_book, initial_quantities, add_quantities, expected_quantities):
        if initial_quantities > 0:
            empty_cart.add_product(product_book, initial_quantities)

        if add_quantities is not None:
            empty_cart.add_product(product_book, add_quantities)
        else:
            empty_cart.add_product(product_book)

        assert product_book in empty_cart.products
        assert empty_cart.products[product_book] == expected_quantities

    def test_remove_product_cart(self, cart_with_products, product_book, product_newspaper):
        cart_with_products.remove_product(product_book, 5)
        assert cart_with_products.products[product_book] == DEFAULT_BUY_COUNT - 5

        cart_with_products.remove_product(product_book)
        assert product_book not in cart_with_products.products

        cart_with_products.remove_product(product_newspaper, DEFAULT_BUY_COUNT + 1)
        assert product_newspaper not in cart_with_products.products

    def test_clear_cart(self, cart_with_products):
        cart_with_products.clear()
        assert len(cart_with_products.products) == 0

    def test_get_total_price_cart(self, empty_cart, cart_with_products):
        assert empty_cart.get_total_price() == 0.0
        assert isinstance(cart_with_products.get_total_price(), float)
        assert cart_with_products.get_total_price() == DEFAULT_BUY_COUNT * (PRICE_BOOK + PRICE_NEWSPAPER)

    def test_buy_cart(self, cart_with_products, product_book, product_newspaper):
        cart_with_products.buy()
        assert product_book.quantity == QUANTITY_BOOK - DEFAULT_BUY_COUNT
        assert product_newspaper.quantity == QUANTITY_NEWSPAPER - DEFAULT_BUY_COUNT
        assert len(cart_with_products.products) == 0

    def test_buy_cart_rase_value_error(self, empty_cart, product_newspaper):
        empty_cart.add_product(product_newspaper, QUANTITY_NEWSPAPER + 1)
        with pytest.raises(ValueError):
            empty_cart.buy()
