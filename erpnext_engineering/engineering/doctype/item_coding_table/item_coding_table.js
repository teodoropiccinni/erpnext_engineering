// Copyright (c) 2025, Teodoro PICCINNI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Coding Table", {
// 	refresh(frm) {
// 	},
	validate: function(frm) {
		let coding_code = frm.doc.engineering_item_coding_table_code || "000";
		let liv1 = frm.doc.engineering_item_coding_table_liv1 || "";
		let liv2 = frm.doc.engineering_item_coding_table_liv2 || "";

		let title = coding_code;
		if (liv1 && liv2) {
			title += ` (${liv1} - ${liv2})`;
		} else if (liv1) {
			title += ` (${liv1})`;
		}

		frm.set_value('engineering_item_coding_table_title', title);
	}

});
