<?php
declare(strict_types=1);

namespace App\Tests;

use App\Discount;
use App\OrderItem;
use App\Order;

class OrderTest extends AbstractOrderTest
{
    public function testPlaceOrderWithSeveralIdenticalItems(): void
    {
        $orderItems = [];
        $orderItemsQuantity = [];
        $order = new Order();
        $orderItem = new OrderItem(1, 'Штаны', 43.3);

        $order->addItem($orderItem);
        $orderItems[$orderItem->getId()] = $orderItem;
        $orderItemsQuantity[$orderItem->getId()] = 1;

        $this->assertOrderAccuracy($order, 43.3, 43.3, $orderItems, $orderItemsQuantity);

        $order->addItem($orderItem);
        $orderItemsQuantity[$orderItem->getId()] = 2;

        $this->assertOrderAccuracy($order, 86.6, 86.6, $orderItems, $orderItemsQuantity);

        $order->increaseItemQuantity($orderItem->getId());
        $orderItemsQuantity[$orderItem->getId()] = 3;

        $this->assertOrderAccuracy($order, 129.9, 129.9, $orderItems, $orderItemsQuantity);

        $order->decreaseItemQuantity($orderItem->getId());
        $orderItemsQuantity[$orderItem->getId()] = 2;

        $this->assertOrderAccuracy($order, 86.6, 86.6, $orderItems, $orderItemsQuantity);

        $order->decreaseItemQuantity($orderItem->getId());
        $order->decreaseItemQuantity($orderItem->getId());

        $this->assertOrderAccuracy($order, 0, 0, [], []);
    }

    public function testPlaceOrderWithItems(): void
    {
        $orderItems = [];
        $orderItemsQuantity = [];
        $order = new Order();
        $orderItem1 = new OrderItem(1, 'Футболка', 89.01);
        $orderItem2 = new OrderItem(2, 'Штаны', 43.30);

        $order->addItem($orderItem1);
        $orderItems[$orderItem1->getId()] = $orderItem1;
        $orderItemsQuantity[$orderItem1->getId()] = 1;

        $this->assertOrderAccuracy($order, 89.01, 89.01, $orderItems, $orderItemsQuantity);

        $order->addItem($orderItem2);
        $orderItems[$orderItem2->getId()] = $orderItem2;
        $orderItemsQuantity[$orderItem2->getId()] = 1;

        $this->assertOrderAccuracy($order, 132.31, 132.31, $orderItems, $orderItemsQuantity);

        $order->increaseItemQuantity($orderItem1->getId());
        $orderItemsQuantity[$orderItem1->getId()] = 2;

        $this->assertOrderAccuracy($order, 221.32, 221.32, $orderItems, $orderItemsQuantity);

        $order->deleteItem($orderItem1->getId());
        unset($orderItems[$orderItem1->getId()]);
        unset($orderItemsQuantity[$orderItem1->getId()]);

        $this->assertOrderAccuracy($order, 43.3, 43.3, $orderItems, $orderItemsQuantity);

        $order->deleteItem($orderItem2->getId());

        $this->assertOrderAccuracy($order, 0, 0, [], []);
    }

    public function testAddDiscountToOrder(): void
    {
        $orderItems = [];
        $orderItemsQuantity = [];
        $discounts = [];
        $order = new Order();
        $orderItem = new OrderItem(3, 'Штаны', 43.3);
        $discount = new Discount(1, 'Скидка на штаны', ['Штаны'], 0.1);

        $order->addItem($orderItem);
        $order->addDiscount($discount);
        $orderItems[$orderItem->getId()] = $orderItem;
        $orderItemsQuantity[$orderItem->getId()] = 1;
        $discounts[$discount->getId()] = $discount;

        $this->assertOrderAccuracy($order, 43.3, 38.97, $orderItems, $orderItemsQuantity, $discounts);

        $order->addItem($orderItem);
        $orderItemsQuantity[$orderItem->getId()] = 2;

        $this->assertOrderAccuracy($order, 86.6, 77.94, $orderItems, $orderItemsQuantity, $discounts);

        $newDiscount = new Discount(2, 'Скидка на все', [], 0.2);
        $order->addDiscount($newDiscount);
        $discounts[$newDiscount->getId()] = $newDiscount;

        $this->assertOrderAccuracy($order, 86.6, 69.28, $orderItems, $orderItemsQuantity, $discounts);

        $order->addDiscount($newDiscount);
        $this->assertOrderAccuracy($order, 86.6, 69.28, $orderItems, $orderItemsQuantity, $discounts);

        $discountForShirts = new Discount(3, 'Скидка на футболки', ['Футболка'], 0.3);
        $order->addDiscount($discountForShirts);
        $discounts[$discountForShirts->getId()] = $discountForShirts;

        $this->assertOrderAccuracy($order, 86.6, 69.28, $orderItems, $orderItemsQuantity, $discounts);

        $order->removeDiscount($newDiscount->getId());
        unset($discounts[$newDiscount->getId()]);

        $this->assertOrderAccuracy($order, 86.6, 77.94, $orderItems, $orderItemsQuantity, $discounts);
    }

    public function testCallForNonExistsProduct(): void
    {
        $order = new Order();
        $orderItem = new OrderItem(1, 'Штаны', 43.3);
        $order->addItem($orderItem);

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Failed to find item #2 in order');
        $order->increaseItemQuantity(2);
    }
}