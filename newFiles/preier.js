// a = [
//   { $match: { orgId: "65028ff6c4569a458cd26192" } },
//   {
//     $project: {
//       "Max_Self_Transfer_for_Debit_Transations": { $ifNull: ["$Max_Self_Transfer_for_Debit_Transations", ""] },
//       Max_Cash_Deposite_for_Debit_Transations: { $ifNull: ["$Max_Cash_Deposite_for_Debit_Transations", ""] },
//       Max_Others_for_Debit_Transations: { $ifNull: ["$Max_Others_for_Debit_Transations", ""] },
//       Max_Cheque_Amount_for_Debit_Transations: { $ifNull: ["$Max_Cheque_Amount_for_Debit_Transations", ""] },
//       Max_UPI_for_Debit_Transations: { $ifNull: ["$Max_UPI_for_Debit_Transations", ""] },
//       "Total_Amount_Self_Transfer_for_Debit_Transations": { $ifNull: ["$Total_Amount_Self_Transfer_for_Debit_Transations", ""] },
//       Total_Cheque_Amount_for_Debit_Transations: { $ifNull: ["$Total_Cheque_Amount_for_Debit_Transations", ""] },
//       Total_Amount_UPI_for_Debit_Transations: { $ifNull: ["$Total_Amount_UPI_for_Debit_Transations", ""] },
//       Total_Amount_Cash_Withdrawals: { $ifNull: ["$Total_Amount_Cash_Withdrawals", ""] },
//       Total_Amount_Others_for_Debit_Transations: { $ifNull: ["$Total_Amount_Others_for_Debit_Transations", ""] },
//       DirName: { $ifNull: ["$DirName", ""] },
//     },
//   },
// ];

b = [
  { $match: { orgId: "65028ff6c4569a458cd26192" } },
  {
    $project: {
      "Transation Date": { $ifNull: ["$Txn_Date", ""] },
      "Cheque / Ref No": { $ifNull: ["$Chq_Ref_No", ""] },
      "Transation Note": { $ifNull: ["$Transation_Note", ""] },
      Amount: { $ifNull: ["$Amount", ""] },
      Transation_Channel: { $ifNull: ["$Transation_Channel", ""] },
      Balance: { $ifNull: ["$Balance", ""] },
      Transation_Type: { $ifNull: ["$Transation_Type", ""] },
    },
  },
];
console.log(JSON.parse);
