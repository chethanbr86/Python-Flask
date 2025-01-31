#part1
# Fetch all distinct sub-categories for dropdown
sub_categories1 = db.session.query(IncomeExpenseManager.sub_category).filter(IncomeExpenseManager.category == "expense").distinct().all()
sub_categories1 = [row[0] for row in sub_categories1]  # Extract values
# When querying with SQLAlchemy, .all() returns a list of tuples, even if you're selecting a single column.
# The [row[0] for row in sub_categories] unpacks the tuples and makes it a list by extracting only the first element, making it easier to use in dropdowns or filters.

# Get selected sub-category from the request
selected_sub_category1 = request.args.get('sub_category', sub_categories1[0] if sub_categories1 else None)

# Query filtered data based on selected sub-category
sub_cat_des_summary1 = (db.session.query(IncomeExpenseManager.sub_category, IncomeExpenseManager.description, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.sub_category == selected_sub_category1).filter(IncomeExpenseManager.category == "expense").group_by(IncomeExpenseManager.sub_category, IncomeExpenseManager.description).order_by(db.func.sum(IncomeExpenseManager.amount).desc()).all())

#part2
sub_categories2 = db.session.query(IncomeExpenseManager.sub_category).filter(IncomeExpenseManager.category == "saving").distinct().all()
sub_categories2 = [row[0] for row in sub_categories2]
selected_sub_category2 = request.args.get('sub_category', sub_categories2[0] if sub_categories2 else None)
sub_cat_des_summary2 = (db.session.query(IncomeExpenseManager.sub_category, IncomeExpenseManager.description, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.sub_category == selected_sub_category2).filter(IncomeExpenseManager.category == "saving").group_by(IncomeExpenseManager.sub_category, IncomeExpenseManager.description).order_by(db.func.sum(IncomeExpenseManager.amount).desc()).all())

#part3
sub_categories3 = db.session.query(IncomeExpenseManager.sub_category).filter(IncomeExpenseManager.category == "investment").distinct().all()
sub_categories3 = [row[0] for row in sub_categories3]
selected_sub_category3 = request.args.get('sub_category', sub_categories3[0] if sub_categories3 else None)
sub_cat_des_summary3 = (db.session.query(IncomeExpenseManager.sub_category, IncomeExpenseManager.description, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.sub_category == selected_sub_category3).filter(IncomeExpenseManager.category == "investment").group_by(IncomeExpenseManager.sub_category, IncomeExpenseManager.description).order_by(db.func.sum(IncomeExpenseManager.amount).desc()).all())

#part4
sub_categories4 = db.session.query(IncomeExpenseManager.sub_category).filter(IncomeExpenseManager.category == "income").distinct().all()
sub_categories4 = [row[0] for row in sub_categories4]
selected_sub_category4 = request.args.get('sub_category', sub_categories4[0] if sub_categories4 else None)
sub_cat_des_summary4 = (db.session.query(IncomeExpenseManager.sub_category, IncomeExpenseManager.description, db.func.sum(IncomeExpenseManager.amount).label('total_amount')).filter(IncomeExpenseManager.sub_category == selected_sub_category4).filter(IncomeExpenseManager.category == "income").group_by(IncomeExpenseManager.sub_category, IncomeExpenseManager.description).order_by(db.func.sum(IncomeExpenseManager.amount).desc()).all())

sub_cat_des_summary1=sub_cat_des_summary1, sub_categories1=sub_categories1, selected_sub_category1=selected_sub_category1, sub_cat_des_summary2=sub_cat_des_summary2, sub_categories2=sub_categories2, selected_sub_category2=selected_sub_category2, sub_cat_des_summary3=sub_cat_des_summary3, sub_categories3=sub_categories3, selected_sub_category3=selected_sub_category3, sub_cat_des_summary4=sub_cat_des_summary4, sub_categories4=sub_categories4, selected_sub_category4=selected_sub_category4,