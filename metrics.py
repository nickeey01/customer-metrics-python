from datetime import datetime

def get_customer_metrics(data, from_, to, min_total_spend=None):
    """
    Calculates customer-level metrics from order data within a date range.
    
    Parameters:
    - data: list of order objects (dicts)
    - from_: start date string (YYYY-MM-DD, inclusive)
    - to: end date string (YYYY-MM-DD, inclusive)
    - min_total_spend: minimum total spend per customer (optional)
    """
    # Dictionary to aggregate customer data: { customer_id: [order_values] }
    customer_orders = {}
    
    # Parse boundary dates for direct comparison if needed, 
    # but string comparison works perfectly for YYYY-MM-DD format.
    for order in data:
        order_date = order.get('orderDate')
        
        # 1. Date filtering (inclusive)
        if not order_date or not (from_ <= order_date <= to):
            continue
            
        customer_id = order.get('customerId')
        if not customer_id:
            continue
            
        # 2. Calculate Order Amount = sum(quantity * unitPrice) across all line items
        # Dynamic check for common line item keys ('items' or 'lineItems')
        items = order.get('items') or order.get('lineItems') or []
        order_amount = sum(
            item.get('quantity', 0) * item.get('unitPrice', 0.0) 
            for item in items
        )
        
        # Group order values by customer
        if customer_id not in customer_orders:
            customer_orders[customer_id] = []
        customer_orders[customer_id].append(order_amount)
        
    results = []
    
    # 3. Calculate per-customer metrics
    for customer_id, order_values in customer_orders.items():
        order_count = len(order_values)
        total_spend = sum(order_values)
        avg_order_value = total_spend / order_count if order_count > 0 else 0.0
        
        # 4. Filter by min_total_spend if provided
        if min_total_spend is not None and total_spend < min_total_spend:
            continue
            
        results.append({
            "customerId": customer_id,
            "orderCount": order_count,
            "totalSpend": total_spend,
            "avgOrderValue": avg_order_value
        })
        
    # 5. Results must be sorted by customerId ascending
    results.sort(key=lambda x: x["customerId"])
    
    return results
