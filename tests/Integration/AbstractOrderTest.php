<?php
declare(strict_types=1);

namespace App\Tests;

use App\Discount;
use App\Order;
use App\OrderItem;
use PHPUnit\Framework\TestCase;

abstract class AbstractOrderTest extends TestCase
{
    private const DELTA = 0.01;

    public function assertOrderAccuracy(Order $order, float $subtotal, float $total, array $orderItems, array $itemsQuantity, array $discounts = []): void
    {
        ksort($orderItems);
        ksort($discounts);

        $this->assertCloseTo($subtotal, $order->getSubtotal());
        $this->assertCloseTo($total, $order->getTotal());
        $this->assertOrderItems($orderItems, $order->getItems());
        $this->assertEquals($itemsQuantity, $order->getItemsQuantity());
        $this->assertOrderDiscounts($discounts, $order->getDiscounts());
    }

    private function assertOrderItems(array $expectedItems, array $actualItems): void
    {
        /** @var OrderItem $expectedItem */
        foreach ($expectedItems as $itemId => $expectedItem)
        {
            /** @var OrderItem $actualItem */
            $actualItem = $actualItems[$itemId];
            $this->assertEquals($expectedItem->getId(), $actualItem->getId());
            $this->assertEquals($expectedItem->getName(), $actualItem->getName());
            $this->assertEquals($expectedItem->getPrice(), $actualItem->getPrice());
        }
    }

    private function assertOrderDiscounts(array $expectedDiscounts, array $actualDiscounts): void
    {
        /** @var Discount $expectedDiscount */
        foreach ($expectedDiscounts as $discountId => $expectedDiscount)
        {
            /** @var Discount $actualDiscount */
            $actualDiscount = $actualDiscounts[$discountId];
            $this->assertEquals($expectedDiscount->getId(), $actualDiscount->getId());
            $this->assertEquals($expectedDiscount->getName(), $actualDiscount->getName());
            $this->assertEquals($expectedDiscount->getDiscountProducts(), $actualDiscount->getDiscountProducts());
            $this->assertCloseTo($expectedDiscount->getAmount(), $actualDiscount->getAmount());
        }
    }

    private function assertCloseTo(float $expected, float $actual): void
    {
        $diff = abs($expected - $actual);
        $this->assertLessThanOrEqual(self::DELTA, $diff);
    }
}