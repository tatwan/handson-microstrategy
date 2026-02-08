# Lab 3: Building a Multi-Dataset Pizza Analytics Dashboard in MicroStrategy

## 1. Introduction and Lab Objectives

In the previous labs, we worked with a single dataset to build visualizations and explore MicroStrategy's core features. In this lab, we take a significant step forward by working with **multiple related datasets** to build a comprehensive analytics dashboard. This mirrors real-world scenarios where business data is rarely contained in a single table — instead, it is distributed across multiple sources that must be joined and linked to tell a complete story.

We will use a pizza restaurant dataset consisting of four CSV files that together describe the restaurant's menu, order history, and sales details. Through this lab, you will learn to:

- **Wrangle data** using MicroStrategy's Data Wrangling tools (duplicate columns, find-and-replace)
- **Create Multi-Form Attributes** to combine an ID field with its descriptive label
- **Import multiple datasets** and configure them for analysis
- **Link datasets** using shared attributes to resolve Cartesian join errors
- **Build KPI cards**, **Grid tables**, **Bar charts**, and **Line charts**
- **Create derived metrics** using the Formula Editor
- **Apply ranking and filtering** to isolate top-performing items

## 2. Understanding the Dataset

Our analysis is built on four CSV files that represent a relational data model for a pizza restaurant. Before importing, it is important to understand how these tables relate to each other.

| File                 | Description                                                | Key Fields                                          |
| -------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| `pizzas.csv`         | Individual pizza products with size and price               | `pizza_id`, `pizza_type_id`, `size`, `price`        |
| `pizza_types.csv`    | Pizza type catalog with names, categories, and ingredients  | `pizza_type_id`, `name`, `category`, `ingredients`  |
| `orders.csv`         | Order records with date and time                           | `order_id`, `date`, `time`                          |
| `order_details.csv`  | Line items linking orders to specific pizzas and quantities | `order_details_id`, `order_id`, `pizza_id`, `quantity` |

The relationships between these tables are as follows:

- `order_details` connects to `orders` through `order_id`
- `order_details` connects to `pizzas` through `pizza_id`
- `pizzas` connects to `pizza_types` through `pizza_type_id`

These links will be essential later when we need MicroStrategy to query across all four datasets without producing Cartesian join errors.

## 3. Importing and Preparing the `pizzas.csv` Dataset

The `pizzas.csv` file contains a `size` column with abbreviated values (`S`, `M`, `L`). For readability in our dashboard, we will create a descriptive version of this column and combine it with the original using a **Multi-Form Attribute**.

### Importing the File

1. In the Data Set panel, click **New Data** and select **File from Disk**.
2. Choose the `pizzas.csv` file. Click **Prepare Data** (not Finish).

   ![image-20260208201205889](images/image-20260208201205889.png)

### Duplicating and Transforming the Size Column

3. In the Data Wrangling view, right-click the `size` column header and select **Duplicate Column**. This creates a copy of the `size` column.

   ![image-20260208201313381](images/image-20260208201313381.png)

4. Rename the duplicated column to `size_desc`. With `size_desc` selected, use the **Find And Replace Characters In Cell** function to convert the abbreviations to full descriptions:

   ![image-20260208201440619](images/image-20260208201440619.png)

   - Replace `S` with `Small`
   - Replace `M` with `Medium`
   - Replace `L` with `Large`

   Your Script panel should show the following transformations:

   ![image-20260208202735181](images/image-20260208202735181.png)

   ![image-20260208202747668](images/image-20260208202747668.png)

### Creating a Multi-Form Attribute

A **Multi-Form Attribute** allows you to combine two related fields — such as an ID and a description — into a single logical attribute. When used in a visualization, MicroStrategy will display both forms together automatically.

5. Go back to the Data Editor, select both **size** and **size desc**, right-click, and select **Create Multi-form Attribute**.

   ![image-20260208202823458](images/image-20260208202823458.png)

6. MicroStrategy will display the two forms: the `ID` form (the original abbreviation) and the `DESC` form (the full description).

   ![image-20260208203008813](images/image-20260208203008813.png)

   ![image-20260208203039033](images/image-20260208203039033.png)

7. Click **Submit**. Notice the **size** attribute now consists of two fields. Click **Update Dataset**.

   ![image-20260208203113386](images/image-20260208203113386.png)

8. You may be asked to confirm the data source. Click **OK** to proceed.

   ![image-20260208203200624](images/image-20260208203200624.png)

9. **Verification:** Drag the **size** attribute onto the canvas. Notice it will automatically show both the ID and description forms.

   ![image-20260208203239941](images/image-20260208203239941.png)

10. Rename `Row Count - pizzas.csv` to `Number of Pizzas`.

    ![image-20260208204332976](images/image-20260208204332976.png)

## 4. Adding the Remaining Datasets

With `pizzas.csv` configured, we now import the three remaining datasets. Each requires a slightly different level of preparation.

### Adding `pizza_types.csv`

1. In the Data Set panel, click **New Data** and import the `pizza_types.csv` file. Click **Finish** — no additional preparation is needed.

   ![image-20260208203732208](images/image-20260208203732208.png)

2. Create a new Page and inspect the pizza types to verify the data loaded correctly.

   ![image-20260208204226958](images/image-20260208204226958.png)

3. Rename `Row Count - pizza_types.csv` to `Number of Pizza Types`.

### Adding `orders.csv`

4. Import `orders.csv`. Nothing needs to be updated — you can load it as is. Rename `Row Count - orders.csv` to `Number of Orders`.

### Adding `order_details.csv`

5. Import `order_details.csv` and click **Prepare Data**. Notice that `quantity` has been incorrectly identified as an **attribute** rather than a **metric**. Right-click `quantity` and select **Convert to Metric**, then click **Finish**.

   ![image-20260208205124518](images/image-20260208205124518.png)

## 5. Linking Datasets with Shared Attributes

At this point, all four datasets are loaded but **isolated from each other**. If you try to drag attributes from different datasets onto the same visualization (e.g., `order id` from `orders.csv` and `name` from `pizza_types.csv`), you will encounter a **Cartesian join error**. This occurs because MicroStrategy does not know how the datasets relate to each other.

![image-20260208210138048](images/image-20260208210138048.png)

To resolve this, we must create **links** between datasets using their shared key columns. We will establish three links:

| Link                      | From Dataset       | To Dataset         | Through Column     |
| ------------------------- | ------------------ | ------------------ | ------------------ |
| Orders ↔ Order Details   | `order_details.csv` | `orders.csv`       | `order_id`         |
| Pizzas ↔ Pizza Types     | `pizzas.csv`       | `pizza_types.csv`  | `pizza_type_id`    |
| Order Details ↔ Pizzas   | `order_details.csv` | `pizzas.csv`       | `pizza_id`         |

### Link 1: `order_id` (Order Details → Orders)

1. In the Data Set panel, right-click `order_id` (under `order_details.csv`) and select **Link to Other Dataset...**

   ![image-20260208210738434](images/image-20260208210738434.png)

2. In the **Link Attributes** dialog box, click **Show Attribute Forms** to verify the mapping. You should see `order_id (ID)` linked to `order_id (ID)`. Click **OK**.

   ![image-20260208210926963](images/image-20260208210926963.png)

3. Notice the link icons that now appear next to the linked fields in the Data Set panel.

   ![image-20260208211049076](images/image-20260208211049076.png)

### Link 2: `pizza_type_id` (Pizzas → Pizza Types)

4. Right-click `pizza_type_id` (under `pizzas.csv`) and select **Link to Other Dataset...** to link it to the `pizza_types.csv` dataset through the `pizza_type_id` column.

   ![image-20260208211354289](images/image-20260208211354289.png)

### Link 3: `pizza_id` (Order Details → Pizzas)

5. From `order_details.csv`, right-click `pizza_id` and link it to the `pizzas.csv` dataset through the `pizza_id` column.

   ![image-20260208211555768](images/image-20260208211555768.png)

With all three links established, MicroStrategy can now query across all four datasets seamlessly.

## 6. Building KPI Cards and Derived Metrics

KPI cards provide at-a-glance summary statistics — the executive view of our restaurant's performance. We will create three KPI cards: Total Number of Orders, Number of Ordered Pizzas, and Average Pizzas per Order.

### KPI 1: Total Number of Orders

1. Add a new visualization and select **KPI** from the visualization type menu.

   ![image-20260208212544432](images/image-20260208212544432.png)

2. Drag `Number of Orders` into the KPI. Optionally, format the number to use a thousands separator (right-click the metric > **Number Format** > enable **Use 1000 Separator**).

   ![image-20260208213916926](images/image-20260208213916926.png)

### KPI 2: Number of Ordered Pizzas

3. Add another **KPI** card. Drag `quantity` (from `order_details.csv`) into it. Name this KPI `Number of Ordered Pizzas`.

   ![image-20260208213320545](images/image-20260208213320545.png)

4. To break this KPI down by pizza category, drag `category` (from `pizza_types.csv`) into the **Break By** zone.

   ![image-20260208214537744](images/image-20260208214537744.png)

5. Drag `date` into the **Trend** zone and resize the KPI card by dragging it downward to give it more display space.

   ![image-20260208214658594](images/image-20260208214658594.png)

### KPI 3: Average Pizzas per Order (Derived Metric)

6. Create a new metric by switching to the **Formula Editor**. Enter the formula:

   ```
   quantity / [Number of Orders]
   ```

   Click **Validate** to confirm the formula is correct, then click **Save**.

7. Add this derived metric as a third KPI card and name it `Average No. Pizzas per Order`. You should now have three KPIs displayed at the top of your dashboard:

   ![image-20260208214417239](images/image-20260208214417239.png)

## 7. Building a Grid Visualization: Pizzas by Price

A **Grid** visualization displays data in a tabular format, ideal for detailed inspection of individual records.

1. Add a new **Grid** visualization below the KPI cards.

   ![image-20260208213036241](images/image-20260208213036241.png)

2. Drag the following fields into the Grid: `name`, `size`, and `price`. Format the price column as currency if desired.

3. Name the visualization `Pizzas by Price`.

   ![image-20260208220216987](images/image-20260208220216987.png)

## 8. Building a Top 5 Selling Pizzas Chart

To identify the restaurant's best sellers, we will create a **Horizontal Bar Chart** filtered to display only the top 5 pizzas by quantity sold. This requires using MicroStrategy's **Rank** function and a visualization-level filter.

### Creating the Bar Chart

1. Add a **Horizontal Bar Chart** to the right of the Grid visualization.

2. Drag `name` to the vertical axis and `quantity` to the horizontal axis.

### Creating a Rank Metric

3. Create a new metric using the **Rank** function on `quantity`. Name it `Rank for Quantity`. Sort the chart descending by `quantity`.

   ![image-20260208221133977](images/image-20260208221133977.png)

### Filtering to Top 5

4. Add the `Rank for Quantity` metric as a **filter** to the visualization (not a global filter).

   ![image-20260208221240512](images/image-20260208221240512.png)

5. Click **Add Qualification**. In the **New Qualification** window:
   - Set **Based on** to the `Rank for Quantity` metric
   - Set **Operator** to `Less than or equal to`
   - Set **Value** to `5`

   ![image-20260208221323487](images/image-20260208221323487.png)

6. Click **Save**.

### Correcting the Rank Order

7. If the results do not show the top sellers as expected, inspect the `Rank for Quantity` metric and change the **Rank Order** from Ascending to **Descending**.

   ![image-20260208221723911](images/image-20260208221723911.png)

8. Name this visualization `Top 5 Selling Pizzas`. Rearrange the KPIs to be on the same row to create more space for the visualizations below.

   ![image-20260208222108987](images/image-20260208222108987.png)

## 9. Analyzing Order Trends Over Time

To observe seasonal patterns and monthly fluctuations in order volume, we will add a **Line Chart** that plots the number of orders over time.

### Generating Date Attributes

1. Right-click the `date` field (from `orders.csv`) to generate new date-based attributes such as `Month of Year` and `Month`.

   ![image-20260208222320204](images/image-20260208222320204.png)

### Building the Line Chart

2. Add a new **Line** chart visualization.

3. Replace the raw `date` field with the `date (Month)` field to aggregate orders at the monthly level. Drag `Number of Orders` to the vertical axis.

4. Name this visualization `Number of Orders per Month`.

## 10. Creating the Order Volume Metric

As a final exercise, create a derived metric called `Order Volume` that calculates the total revenue per line item. In the Formula Editor, enter:

```
Order Volume = Quantity x Price
```

This metric multiplies the number of pizzas ordered by their unit price, giving you a revenue figure that can be used in further analysis.

## Final Dashboard

Your completed dashboard should include the following components:

- **3 KPI Cards** at the top: Total Number of Orders, Number of Ordered Pizzas (broken down by category with trend), and Average No. Pizzas per Order
- **Pizzas by Price** Grid table (left)
- **Top 5 Selling Pizzas** Horizontal Bar Chart (right)
- **Number of Orders per Month** Line Chart (bottom)

![image-20260208222654708](images/image-20260208222654708.png)

### Conclusion

Save your Dossier. In this lab, you successfully built a multi-dataset analytics dashboard from four separate CSV files. You learned how to wrangle raw data, create multi-form attributes for cleaner display, link datasets through shared keys to avoid Cartesian join errors, and build a variety of visualizations including KPI cards, grids, ranked bar charts, and time-series line charts. These skills form the foundation for working with relational data models in MicroStrategy.
