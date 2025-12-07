#!/usr/bin/env python3
"""
Stripe Integration Field Mapping Documentation
==============================================

This script documents the complete field mapping from:
1. Stripe Raw Data -> RootFi Data Model
2. RootFi Data Model -> Sales Tax API Model

Run this script to see the complete mapping documentation.
"""

# =============================================================================
# PARSER FUNCTIONS (Pseudocode)
# =============================================================================

PARSER_FUNCTIONS = {
    "STRIPE_DATE_PARSER": """
    def STRIPE_DATE_PARSER(timestamp: int) -> str | None:
        '''Converts Unix timestamp (seconds) to ISO 8601 date string'''
        if not timestamp:
            return None
        return datetime.fromtimestamp(timestamp).isoformat()
        # Example: 1699900800 -> "2023-11-13T12:00:00.000Z"
    """,
    
    "STRIPE_CURRENCY_PARSER": """
    def STRIPE_CURRENCY_PARSER(currency_code: str) -> str | None:
        '''Converts lowercase currency code to uppercase ISO 4217'''
        if not currency_code:
            return None
        return currency_code.upper()
        # Example: "usd" -> "USD"
    """,
    
    "STRIPE_AMOUNT_PARSER": """
    def STRIPE_AMOUNT_PARSER(value: int, record, stack) -> float | None:
        '''Converts cents to dollars using currency-aware logic'''
        if value is None:
            return None
        
        # Get currency from record or parent stack
        if record.object in ['invoice', 'credit_note']:
            currency = record.currency
        elif record.object in ['line_item', 'credit_note_line_item']:
            currency = stack[1].currency  # Parent invoice/credit_note
        
        # Use CurrencyHandler to convert from smallest unit
        return CurrencyHandler.fromLowerDenominator(value, currency)
        # Example: 1000 (cents) with USD -> 10.00 (dollars)
    """,
    
    "STRIPE_RATE_PARSER": """
    def STRIPE_RATE_PARSER(value: float) -> float | None:
        '''Converts percentage to decimal (e.g., 8.25% -> 0.0825)'''
        if value is None:
            return None
        return value / 100
        # Example: 8.25 -> 0.0825
    """,
    
    "STRIPE_PRODUCT_STATUS_PARSER": """
    def STRIPE_PRODUCT_STATUS_PARSER(active: bool) -> str:
        '''Converts boolean active flag to status string'''
        if active:
            return "ACTIVE"
        return "ARCHIVED"
    """,
    
    "STRIPE_PAYMENT_STATUS_PARSER": """
    def STRIPE_PAYMENT_STATUS_PARSER(record) -> str | None:
        '''Maps Stripe PaymentIntent status to RootFi payment status'''
        if record.last_payment_error:
            return "FAILED"
        
        status_map = {
            "requires_payment_method": "CREATED",
            "canceled": "CREATED",
            "requires_confirmation": "ATTEMPTED",
            "requires_capture": "ATTEMPTED",
            "requires_action": "ATTEMPTED",
            "processing": "ATTEMPTED",
            "succeeded": "PAID"
        }
        return status_map.get(record.status)
    """,
    
    "STRIPE_TOTAL_TAX_AMOUNT_PARSER": """
    def STRIPE_TOTAL_TAX_AMOUNT_PARSER(value, record, stack) -> float | None:
        '''Aggregates all tax amounts from invoice/line item'''
        tax_amounts = []
        
        if record.object in ['invoice', 'credit_note']:
            tax_amounts = record.total_tax_amounts or record.tax_amounts or []
            currency = record.currency
        elif record.object in ['line_item', 'credit_note_line_item']:
            tax_amounts = record.tax_amounts or []
            currency = stack[1].currency
        
        total = sum(item.amount for item in tax_amounts)
        return CurrencyHandler.fromLowerDenominator(total, currency)
    """,
    
    "STRIPE_TOTAL_DISCOUNT_AMOUNT_PARSER": """
    def STRIPE_TOTAL_DISCOUNT_AMOUNT_PARSER(value, record, stack) -> float | None:
        '''Aggregates all discount amounts from invoice/line item'''
        discount_amounts = []
        
        if record.object in ['invoice', 'credit_note']:
            discount_amounts = record.total_discount_amounts or record.discount_amounts or []
            currency = record.currency
        elif record.object in ['line_item', 'credit_note_line_item']:
            discount_amounts = record.discount_amounts or []
            currency = stack[1].currency
        
        total = sum(item.amount for item in discount_amounts)
        return CurrencyHandler.fromLowerDenominator(total, currency)
    """,
    
    "STRIPE_CONTACT_ADDRESS_PARSER": """
    def STRIPE_CONTACT_ADDRESS_PARSER(value, customer, stack, rootfiParser) -> list:
        '''Extracts billing and shipping addresses from customer'''
        addresses = []
        
        if customer.address:
            billing = mapAddress(customer.address, "BILLING", rootfiParser.data_model, customer.id)
            addresses.append(billing)
        
        if customer.shipping and customer.shipping.address:
            shipping = mapAddress(customer.shipping.address, "SHIPPING", rootfiParser.data_model, customer.id)
            addresses.append(shipping)
        
        return addresses
    """,
    
    "STRIPE_ITEM_ID_PARSER": """
    def STRIPE_ITEM_ID_PARSER(value, record, stack, rootfiParser) -> str | None:
        '''Extracts product ID from line item price object'''
        return record.price.product if record.price else record.pricing.price_details.product
    """
}

# =============================================================================
# CUSTOMER MAPPING
# =============================================================================

CUSTOMER_MAPPING = {
    "description": "Maps Stripe Customer to RootFi PAYMENT_CUSTOMERS to Sales Tax Customer",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "cus_ABC123",
            "notes": "Stripe customer ID"
        },
        "platform_unique_id": {
            "stripe_field": "id",
            "example": "cus_ABC123",
            "notes": "Same as platform_id"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER",
            "example_input": 1699900800,
            "example_output": "2023-11-13T12:00:00.000Z",
            "notes": "Unix timestamp (seconds) to ISO date"
        },
        "updated_at": {
            "stripe_field": "_",
            "notes": "Not available from Stripe, set to null"
        },
        "name": {
            "stripe_field": "name",
            "example": "John Doe"
        },
        "tax_number": {
            "stripe_field": "tax_ids.data.0.value",
            "example": "US123456789",
            "notes": "First tax ID value from expanded tax_ids"
        },
        "currency_id": {
            "stripe_field": "currency",
            "parser": "STRIPE_CURRENCY_PARSER",
            "example_input": "usd",
            "example_output": "USD"
        },
        "addresses": {
            "stripe_field": "_",
            "parser": "STRIPE_CONTACT_ADDRESS_PARSER",
            "notes": "Extracts from customer.address (billing) and customer.shipping.address (shipping)"
        },
        "phone_numbers": {
            "stripe_field": "_",
            "parser": "STRIPE_CONTACT_PHONE_NUMBERS_PARSER",
            "notes": "Extracts from customer.phone"
        },
        "external_links": {
            "stripe_field": "_",
            "parser": "STRIPE_CONTACT_EXTERNAL_LINKS_PARSER",
            "notes": "Extracts email from customer.email"
        }
    },
    
    "rootfi_to_sales_tax": {
        "ID": {
            "source": "Generated UUID",
            "notes": "New UUID generated by Sales Tax API"
        },
        "Name": {
            "source": "RootFi name field",
            "notes": "Direct mapping"
        },
        "Email": {
            "source": "RootFi external_links (EMAIL type)",
            "notes": "Extracted from external links"
        },
        "SourcePlatformID": {
            "source": "RootFi platform_id",
            "notes": "Used for lookup: source_platform_id"
        },
        "SourcePlatform": {
            "source": "STRIPE",
            "notes": "Hardcoded integration type"
        },
        "Corporation_id": {
            "source": "From API context",
            "notes": "Corporation making the request"
        },
        "ShippingAddress": {
            "source": "RootFi addresses (SHIPPING type)",
            "notes": "Address with type=SHIPPING"
        }
    }
}

# =============================================================================
# PRODUCT MAPPING
# =============================================================================

PRODUCT_MAPPING = {
    "description": "Maps Stripe Product to RootFi PAYMENT_ITEMS/PAYMENT_PRODUCTS to Sales Tax Product",
    
    "stripe_to_rootfi_items": {
        "platform_id": {
            "stripe_field": "id",
            "example": "prod_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id",
            "example": "prod_ABC123"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "name": {
            "stripe_field": "name",
            "example": "Premium Widget"
        },
        "description": {
            "stripe_field": "description",
            "example": "A high-quality widget"
        },
        "code": {
            "stripe_field": "_",
            "notes": "Not available from Stripe"
        },
        "unit_price": {
            "stripe_field": "default_price.unit_amount",
            "notes": "From expanded default_price, in cents"
        },
        "updated_at": {
            "stripe_field": "_",
            "notes": "Not available"
        },
        "currency_id": {
            "stripe_field": "default_price.currency",
            "parser": "STRIPE_CURRENCY_PARSER"
        },
        "status": {
            "stripe_field": "active",
            "parser": "STRIPE_PRODUCT_STATUS_PARSER",
            "example_input": True,
            "example_output": "ACTIVE",
            "notes": "true -> ACTIVE, false -> ARCHIVED"
        }
    },
    
    "stripe_to_rootfi_products": {
        "platform_id": {
            "stripe_field": "id"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "description": {
            "stripe_field": "description"
        },
        "name": {
            "stripe_field": "name"
        },
        "status": {
            "stripe_field": "active",
            "parser": "STRIPE_PRODUCT_STATUS_PARSER"
        },
        "updated_at": {
            "stripe_field": "updated",
            "parser": "STRIPE_DATE_PARSER"
        }
    },
    
    "rootfi_to_sales_tax": {
        "ID": {
            "source": "Generated UUID"
        },
        "Name": {
            "source": "RootFi name"
        },
        "TaxCode": {
            "source": "Default or configured",
            "notes": "Defaults to 'TPP' if not set. Can be configured per corporation."
        },
        "Sku": {
            "source": "RootFi code or platform_id",
            "notes": "Used for product lookup"
        },
        "Description": {
            "source": "RootFi description"
        },
        "SourcePlatformID": {
            "source": "RootFi platform_id"
        },
        "SourcePlatform": {
            "source": "STRIPE"
        },
        "CorporationId": {
            "source": "From API context"
        }
    }
}

# =============================================================================
# INVOICE/TRANSACTION MAPPING
# =============================================================================

INVOICE_MAPPING = {
    "description": "Maps Stripe Invoice to RootFi PAYMENT_INVOICES to Sales Tax Invoice/Transaction",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "in_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "document_number": {
            "stripe_field": "number",
            "example": "INV-0001"
        },
        "contact_id": {
            "stripe_field": "customer",
            "example": "cus_ABC123",
            "notes": "Stripe customer ID"
        },
        "posted_date": {
            "stripe_field": "effective_at",
            "parser": "STRIPE_DATE_PARSER"
        },
        "due_date": {
            "stripe_field": "due_date",
            "parser": "STRIPE_DATE_PARSER"
        },
        "currency_id": {
            "stripe_field": "currency",
            "parser": "STRIPE_CURRENCY_PARSER"
        },
        "status": {
            "stripe_field": "status",
            "enum_mapper": "ARTIFACT_STATUS_ENUM",
            "notes": "Maps: draft, open, paid, uncollectible, void"
        },
        "sub_total": {
            "stripe_field": "subtotal",
            "parser": "STRIPE_AMOUNT_PARSER",
            "example_input": 10000,
            "example_output": 100.00,
            "notes": "Cents to dollars"
        },
        "tax_amount": {
            "stripe_field": "_",
            "parser": "STRIPE_TOTAL_TAX_AMOUNT_PARSER",
            "notes": "Aggregates total_tax_amounts array"
        },
        "total_discount": {
            "stripe_field": "_",
            "parser": "STRIPE_TOTAL_DISCOUNT_AMOUNT_PARSER",
            "notes": "Aggregates total_discount_amounts array"
        },
        "total_amount": {
            "stripe_field": "total",
            "parser": "STRIPE_AMOUNT_PARSER"
        },
        "amount_due": {
            "stripe_field": "amount_due",
            "parser": "STRIPE_AMOUNT_PARSER"
        },
        "memo": {
            "stripe_field": "description"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "updated_at": {
            "stripe_field": "_",
            "notes": "Not available"
        },
        "line_items": {
            "stripe_field": "lines.data",
            "notes": "Array of line items, mapped separately"
        },
        "addresses": {
            "stripe_field": "_",
            "parser": "STRIPE_INVOICE_ADDRESS_PARSER",
            "notes": "Extracts from customer_address (billing) and customer_shipping.address (shipping)"
        },
        "shipping_amount": {
            "stripe_field": "shipping_cost.amount_total",
            "parser": "STRIPE_AMOUNT_PARSER"
        }
    },
    
    "rootfi_to_sales_tax": {
        "ID": {
            "source": "Generated UUID"
        },
        "CorporationId": {
            "source": "From API context"
        },
        "TransactedAt": {
            "source": "RootFi posted_date"
        },
        "InvoiceCurrency": {
            "source": "RootFi currency_id"
        },
        "Subtotal": {
            "source": "RootFi sub_total"
        },
        "Discount": {
            "source": "RootFi total_discount"
        },
        "ShippingAndHandling": {
            "source": "RootFi shipping_amount"
        },
        "Total": {
            "source": "RootFi total_amount"
        },
        "TaxCollected": {
            "source": "RootFi tax_amount"
        },
        "TransactionType": {
            "source": "Derived from context",
            "notes": "SALE, RETURN, REFUND based on invoice type"
        },
        "SourcePlatform": {
            "source": "STRIPE"
        },
        "SourcePlatformID": {
            "source": "RootFi platform_id"
        },
        "CustomerId": {
            "source": "Resolved from RootFi contact_id",
            "notes": "Looked up by source_platform_id in Sales Tax customers"
        },
        "ShippingAddress": {
            "source": "RootFi addresses (SHIPPING type)"
        }
    }
}

# =============================================================================
# LINE ITEM MAPPING
# =============================================================================

LINE_ITEM_MAPPING = {
    "description": "Maps Stripe Invoice Line Item to RootFi PAYMENT_LINE_ITEMS to Sales Tax LineItem",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "il_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "line_item_type": {
            "stripe_field": "$data_model",
            "notes": "Set to parent data model (PAYMENT_INVOICES, etc.)"
        },
        "line_item_type_id": {
            "stripe_field": "$parent.id",
            "notes": "Parent invoice/credit note ID"
        },
        "description": {
            "stripe_field": "description"
        },
        "item_id": {
            "stripe_field": "_",
            "parser": "STRIPE_ITEM_ID_PARSER",
            "notes": "Extracts from price.product or pricing.price_details.product"
        },
        "total_discount": {
            "stripe_field": "_",
            "parser": "STRIPE_TOTAL_DISCOUNT_AMOUNT_PARSER"
        },
        "tax_amount": {
            "stripe_field": "_",
            "parser": "STRIPE_TOTAL_TAX_AMOUNT_PARSER"
        },
        "quantity": {
            "stripe_field": "quantity",
            "parser": "STRIPE_LINE_ITEM_QUANTITY_PARSER",
            "notes": "Direct pass-through"
        },
        "unit_amount": {
            "stripe_field": "unit_amount_excluding_tax",
            "parser": "STRIPE_LINE_ITEM_UNIT_AMOUNT_PARSER",
            "notes": "Converts from cents"
        },
        "total_amount": {
            "stripe_field": "amount",
            "parser": "STRIPE_AMOUNT_PARSER"
        },
        "tax_id": {
            "stripe_field": "tax_rates.0.id",
            "notes": "First tax rate ID"
        },
        "sub_total": {
            "stripe_field": "amount_excluding_tax",
            "parser": "STRIPE_AMOUNT_PARSER"
        }
    },
    
    "rootfi_to_sales_tax": {
        "ID": {
            "source": "Generated UUID"
        },
        "Amount": {
            "source": "RootFi total_amount"
        },
        "Quantity": {
            "source": "RootFi quantity"
        },
        "Discount": {
            "source": "RootFi total_discount"
        },
        "PricePerUnit": {
            "source": "RootFi unit_amount"
        },
        "TaxCollected": {
            "source": "RootFi tax_amount"
        },
        "TaxCode": {
            "source": "Resolved from product or default",
            "notes": "Looked up from product.tax_code, defaults to 'TPP'"
        },
        "ProductId": {
            "source": "Resolved from RootFi item_id",
            "notes": "Looked up by source_platform_id in Sales Tax products"
        }
    }
}

# =============================================================================
# TAX RATE MAPPING
# =============================================================================

TAX_RATE_MAPPING = {
    "description": "Maps Stripe Tax Rate to RootFi PAYMENT_TAX_RATES",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "txr_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "updated_at": {
            "stripe_field": "updated_at",
            "parser": "STRIPE_DATE_PARSER"
        },
        "name": {
            "stripe_field": "display_name",
            "example": "Sales Tax"
        },
        "description": {
            "stripe_field": "description"
        },
        "rate": {
            "stripe_field": "percentage",
            "parser": "STRIPE_RATE_PARSER",
            "example_input": 8.25,
            "example_output": 0.0825,
            "notes": "Percentage to decimal"
        }
    }
}

# =============================================================================
# REFUND MAPPING
# =============================================================================

REFUND_MAPPING = {
    "description": "Maps Stripe Refund to RootFi PAYMENT_REFUNDS",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "re_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "amount": {
            "stripe_field": "amount",
            "notes": "In cents, NOT converted (raw value)"
        },
        "currency_id": {
            "stripe_field": "currency",
            "parser": "STRIPE_CURRENCY_PARSER"
        },
        "payment_id": {
            "stripe_field": "payment_intent",
            "notes": "Links to PaymentIntent"
        },
        "description": {
            "stripe_field": "reason",
            "notes": "duplicate, fraudulent, requested_by_customer, etc."
        },
        "status": {
            "stripe_field": "status",
            "enum_mapper": "PAYMENTS_REFUND_STATUS_ENUM",
            "notes": "pending, succeeded, failed, canceled"
        }
    }
}

# =============================================================================
# CREDIT NOTE MAPPING
# =============================================================================

CREDIT_NOTE_MAPPING = {
    "description": "Maps Stripe Credit Note to RootFi PAYMENT_CREDIT_NOTES",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "cn_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "contact_id": {
            "stripe_field": "customer"
        },
        "currency_id": {
            "stripe_field": "currency",
            "parser": "STRIPE_CURRENCY_PARSER"
        },
        "document_number": {
            "stripe_field": "number"
        },
        "invoice_ids": {
            "stripe_field": "invoice",
            "notes": "Single invoice ID converted to array"
        },
        "line_items": {
            "stripe_field": "lines.data"
        },
        "memo": {
            "stripe_field": "memo"
        },
        "posted_date": {
            "stripe_field": "effective_at",
            "parser": "STRIPE_DATE_PARSER"
        },
        "status": {
            "stripe_field": "status",
            "enum_mapper": "ARTIFACT_STATUS_ENUM",
            "notes": "issued, void"
        },
        "tax_amount": {
            "stripe_field": "_",
            "parser": "STRIPE_TOTAL_TAX_AMOUNT_PARSER"
        },
        "total_amount": {
            "stripe_field": "total",
            "parser": "STRIPE_AMOUNT_PARSER"
        },
        "total_discount": {
            "stripe_field": "_",
            "parser": "STRIPE_TOTAL_DISCOUNT_AMOUNT_PARSER"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "shipping_amount": {
            "stripe_field": "shipping_cost.amount_total",
            "parser": "STRIPE_AMOUNT_PARSER"
        }
    }
}

# =============================================================================
# PAYMENT MAPPING
# =============================================================================

PAYMENT_MAPPING = {
    "description": "Maps Stripe PaymentIntent to RootFi PAYMENT_PAYMENTS",
    
    "stripe_to_rootfi": {
        "platform_id": {
            "stripe_field": "id",
            "example": "pi_ABC123"
        },
        "platform_unique_id": {
            "stripe_field": "id"
        },
        "amount": {
            "stripe_field": "amount",
            "notes": "In cents, NOT converted"
        },
        "created_at": {
            "stripe_field": "created",
            "parser": "STRIPE_DATE_PARSER"
        },
        "currency_id": {
            "stripe_field": "currency",
            "parser": "STRIPE_CURRENCY_PARSER"
        },
        "customer_id": {
            "stripe_field": "customer.id",
            "notes": "From expanded customer object"
        },
        "invoice_id": {
            "stripe_field": "invoice"
        },
        "payment_method": {
            "stripe_field": "payment_method.type",
            "enum_mapper": "PAYMENTS_PAYMENT_METHOD",
            "notes": "card, upi, link, etc."
        },
        "status": {
            "stripe_field": "status",
            "parser": "STRIPE_PAYMENT_STATUS_PARSER",
            "notes": "Complex mapping based on status and last_payment_error"
        },
        "order_id": {
            "stripe_field": "id",
            "notes": "Same as platform_id"
        },
        "description": {
            "stripe_field": "description"
        }
    }
}

# =============================================================================
# SALES TAX API INTEGRATION FLOW
# =============================================================================

INTEGRATION_FLOW = """
SALES TAX API INTEGRATION FLOW
==============================

1. CUSTOMER RESOLUTION
   - When creating a transaction, the API first tries to resolve the customer:
   
   if customer_details.source_platform and customer_details.source_platform_id:
       customer = GetCustomerBySourcePlatformId(
           corporation_id,
           source_platform,      # "STRIPE"
           source_platform_id    # Stripe customer ID (cus_xxx)
       )
       if customer:
           customer_id = customer.ID

2. PRODUCT RESOLUTION
   - For each line item, products are resolved by source_platform_id:
   
   products = GetProductsBySourcePlatforms(
       corporation_id,
       source_platforms,      # ["STRIPE", "STRIPE", ...]
       source_platform_ids    # [prod_xxx, prod_yyy, ...]
   )
   
   for line_item in line_items:
       for product in products:
           if line_item.product_source_platform_id == product.source_platform_id:
               line_item.product_id = product.ID
               line_item.tax_code = product.tax_code

3. TAX CODE DEFAULTING
   - If product not found or has no tax_code:
   
   if not product or not product.tax_code:
       line_item.tax_code = corporation_config.default_product_taxability_code or "TPP"

4. ADDRESS HANDLING
   - Ship-to address is required for tax calculation
   - Can come from request body or customer's shipping address:
   
   if not ship_to_address and customer and customer.shipping_address:
       ship_to_address = customer.shipping_address

5. TAX CALCULATION
   - Final calculation uses resolved data:
   
   calculation_result = CalculateTax({
       corporation_id,
       transaction_date,
       transaction_currency,
       transaction_type,      # SALE, RETURN, REFUND
       addresses: {
           ship_to_address,
           ship_from_address   # Optional
       },
       customer_details: {
           customer_id        # Resolved Sales Tax customer ID
       },
       line_items: [{
           product_id,        # Resolved Sales Tax product ID
           taxability_code,   # From product or default
           quantity,
           amount,
           discount
       }]
   })
"""

# =============================================================================
# MAIN OUTPUT
# =============================================================================

def print_mapping(name, mapping):
    print(f"\n{'='*80}")
    print(f" {name}")
    print(f"{'='*80}")
    print(f"\nDescription: {mapping.get('description', 'N/A')}\n")
    
    for section_name, section_data in mapping.items():
        if section_name == 'description':
            continue
        print(f"\n--- {section_name.upper()} ---\n")
        for field, details in section_data.items():
            print(f"  {field}:")
            if isinstance(details, dict):
                for key, value in details.items():
                    print(f"    {key}: {value}")
            else:
                print(f"    {details}")
            print()

def print_parsers():
    print(f"\n{'='*80}")
    print(f" PARSER FUNCTIONS (Pseudocode)")
    print(f"{'='*80}")
    for name, code in PARSER_FUNCTIONS.items():
        print(f"\n{name}:")
        print(code)

def main():
    print("""
################################################################################
#                                                                              #
#           STRIPE INTEGRATION FIELD MAPPING DOCUMENTATION                     #
#                                                                              #
#  This document shows the complete field mapping from:                        #
#  1. Stripe Raw Data -> RootFi Data Model                                     #
#  2. RootFi Data Model -> Sales Tax API Model                                 #
#                                                                              #
################################################################################
""")
    
    print_parsers()
    print_mapping("CUSTOMER MAPPING", CUSTOMER_MAPPING)
    print_mapping("PRODUCT MAPPING", PRODUCT_MAPPING)
    print_mapping("INVOICE/TRANSACTION MAPPING", INVOICE_MAPPING)
    print_mapping("LINE ITEM MAPPING", LINE_ITEM_MAPPING)
    print_mapping("TAX RATE MAPPING", TAX_RATE_MAPPING)
    print_mapping("REFUND MAPPING", REFUND_MAPPING)
    print_mapping("CREDIT NOTE MAPPING", CREDIT_NOTE_MAPPING)
    print_mapping("PAYMENT MAPPING", PAYMENT_MAPPING)
    
    print(INTEGRATION_FLOW)
    
    print("""
################################################################################
#                                                                              #
#                           KEY TRANSFORMATIONS SUMMARY                        #
#                                                                              #
################################################################################

1. AMOUNTS: Stripe stores in cents -> Converted to dollars via STRIPE_AMOUNT_PARSER
   Example: 1000 (cents) -> 10.00 (dollars)

2. DATES: Stripe uses Unix timestamps (seconds) -> ISO 8601 strings
   Example: 1699900800 -> "2023-11-13T12:00:00.000Z"

3. CURRENCY: Stripe uses lowercase -> Uppercase ISO 4217
   Example: "usd" -> "USD"

4. TAX RATES: Stripe uses percentage -> Decimal
   Example: 8.25 -> 0.0825

5. PRODUCT STATUS: Boolean -> String enum
   Example: true -> "ACTIVE", false -> "ARCHIVED"

6. PAYMENT STATUS: Complex mapping based on status + error state
   - last_payment_error present -> "FAILED"
   - requires_payment_method/canceled -> "CREATED"
   - requires_confirmation/capture/action/processing -> "ATTEMPTED"
   - succeeded -> "PAID"

7. PRODUCT RESOLUTION: By source_platform_id lookup
   - Stripe product ID (prod_xxx) -> Sales Tax Product UUID
   - If not found, tax_code defaults to "TPP"

8. CUSTOMER RESOLUTION: By source_platform_id lookup
   - Stripe customer ID (cus_xxx) -> Sales Tax Customer UUID
""")

if __name__ == "__main__":
    main()
