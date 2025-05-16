<?php
declare(strict_types=1);

namespace App;

class Order
{
    /** @var OrderItem[] */
    private array $items = [];
    /** @var array<int, int> id -> quantity */
    private array $itemsQuantity = [];
    /** @var Discount[] */
    private array $discounts = [];

    public function addItem(OrderItem $item): void
    {
        if ($this->items[$item->getId()])
        {
            $this->increaseItemQuantity($item->getId());
            return;
        }
        $this->items[$item->getId()] = $item;
        $this->itemsQuantity[$item->getId()] = 1;
        ksort($this->items);
    }

    public function increaseItemQuantity(int $itemId): void
    {
        if (!$this->itemsQuantity[$itemId])
        {
            throw new \InvalidArgumentException("Failed to find item #$itemId in order");
        }
        ++$this->itemsQuantity[$itemId];
    }

    public function decreaseItemQuantity(int $itemId): void
    {
        if (!$this->itemsQuantity[$itemId])
        {
            throw new \InvalidArgumentException("Failed to find item #$itemId in order");
        }
        if ($this->itemsQuantity[$itemId] == 1)
        {
            $this->deleteItem($itemId);
            return;
        }

        --$this->itemsQuantity[$itemId];
    }

    public function deleteItem(int $itemId): void
    {
        if (!$this->itemsQuantity[$itemId])
        {
            throw new \InvalidArgumentException("Failed to find item #$itemId in order");
        }
        unset($this->itemsQuantity[$itemId]);
        unset($this->items[$itemId]);
    }

    public function addDiscount(Discount $discount): void
    {
        if ($this->discounts[$discount->getId()])
        {
            return;
        }

        $this->discounts[$discount->getId()] = $discount;
    }

    public function removeDiscount(int $discountId): void
    {
        if (!$this->discounts[$discountId])
        {
            throw new \InvalidArgumentException("Failed to find discount #$discountId in order");
        }

        unset($this->discounts[$discountId]);
    }

    public function getSubtotal(): float
    {
        $sum = 0.0;

        foreach ($this->items as $itemId => $item)
        {
            $sum += $item->getPrice() * $this->itemsQuantity[$itemId];
        }

        return $sum;
    }

    public function getTotal(): float
    {
        $sum = 0.0;

        foreach ($this->items as $item)
        {
            $maxDiscount = 0.0;

            foreach ($this->discounts as $discount)
            {
                if (!$discount->getDiscountProducts() || in_array($item->getName(), $discount->getDiscountProducts()))
                {
                    $maxDiscount = max($maxDiscount, min($discount->getAmount(), 1.0));
                }
            }

            $sum += $item->getPrice() * $this->itemsQuantity[$item->getId()] * (1.0 - $maxDiscount);
        }

        return $sum;
    }

    /** @return OrderItem[] */
    public function getItems(): array
    {
        return $this->items;
    }

    /** @return array<int, int> id -> quantity */
    public function getItemsQuantity(): array
    {
        return $this->itemsQuantity;
    }

    /** @return Discount[] */
    public function getDiscounts(): array
    {
        return $this->discounts;
    }
}