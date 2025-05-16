<?php
declare(strict_types=1);

namespace App;

readonly class Discount
{
    public function __construct(
        private int $id,
        private string $name,
        private array $discountProducts,
        private float $amount
    ) {
    }

    /**
     * @return int
     */
    public function getId(): int
    {
        return $this->id;
    }

    /**
     * @return string
     */
    public function getName(): string
    {
        return $this->name;
    }

    /**
     * @return string[]
     */
    public function getDiscountProducts(): array
    {
        return $this->discountProducts;
    }

    /**
     * @return float
     */
    public function getAmount(): float
    {
        return $this->amount;
    }
}