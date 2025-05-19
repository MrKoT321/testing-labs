<?php
declare(strict_types=1);

namespace App\Tests\Unit;

use App\Discount;
use App\OrderItem;
use App\Order;
use PHPUnit\Framework\TestCase;

class OrderUnitTest extends TestCase
{
    public function testAddItemIncreasesTotal(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 50.0);

        $order->addItem($item);

        $this->assertEquals(50.0, $order->getSubtotal());
        $this->assertEquals(50.0, $order->getTotal());
    }

    public function testIncreaseItemQuantity(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 50.0);

        $order->addItem($item);
        $order->increaseItemQuantity($item->getId());

        $this->assertEquals(100.0, $order->getSubtotal());
        $this->assertEquals(100.0, $order->getTotal());
    }

    public function testAddSameItem(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 50.0);

        $order->addItem($item);
        $order->addItem($item);

        $this->assertEquals(100.0, $order->getSubtotal());
        $this->assertEquals(100.0, $order->getTotal());
        $this->assertEquals([$item->getId() => 2], $order->getItemsQuantity());
    }

    public function testDecreaseItemQuantityRemovesWhenZero(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 50.0);

        $order->addItem($item);
        $order->decreaseItemQuantity($item->getId());
        $this->assertEquals(0.0, $order->getSubtotal());
        $this->assertEquals([], $order->getItems());
    }

    public function testAddDiscountAffectsTotal(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 100.0);
        $discount = new Discount(1, 'Скидка на штаны', ['Штаны'], 0.2);

        $order->addItem($item);
        $order->addDiscount($discount);

        $this->assertEquals(100.0, $order->getSubtotal());
        $this->assertEquals(80.0, $order->getTotal());
        $this->assertEquals('Скидка на штаны', $order->getDiscounts()[$discount->getId()]->getName());
    }

    public function testAddSameDiscountAffectsTotal(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 100.0);
        $discount = new Discount(1, 'Скидка на штаны', ['Штаны'], 0.2);

        $order->addItem($item);
        $order->addDiscount($discount);
        $order->addDiscount($discount);

        $this->assertEquals(100.0, $order->getSubtotal());
        $this->assertEquals(80.0, $order->getTotal());
    }

    public function testAddNonApplicableDiscountHasNoEffect(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 100.0);
        $discount = new Discount(1, 'Скидка на футболки', ['Футболка'], 0.5);

        $order->addItem($item);
        $order->addDiscount($discount);

        $this->assertEquals(100.0, $order->getTotal());
    }

    public function testGlobalDiscountApplied(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 200.0);
        $discount = new Discount(2, 'Глобальная скидка', [], 0.1);

        $order->addItem($item);
        $order->addDiscount($discount);

        $this->assertEquals(180.0, $order->getTotal());
    }

    public function testRemovingDiscountRestoresOriginalPrice(): void
    {
        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 100.0);
        $discount = new Discount(1, 'Скидка на штаны', ['Штаны'], 0.1);

        $order->addItem($item);
        $order->addDiscount($discount);
        $order->removeDiscount($discount->getId());

        $this->assertEquals(100.0, $order->getTotal());
    }

    public function testIncreaseItemQuantityThrowsOnInvalidId(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Failed to find item #2 in order');

        $order = new Order();
        $item = new OrderItem(1, 'Штаны', 100.0);
        $order->addItem($item);

        $order->increaseItemQuantity(2);
    }
}
