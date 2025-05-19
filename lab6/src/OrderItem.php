<?php
declare(strict_types=1);

namespace App;

readonly class OrderItem
{
    public function __construct(
        private int $id,
        private string $name,
        private float $price
    )
    {}

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
     * @return float
     */
    public function getPrice(): float
    {
        return $this->price;
    }
}