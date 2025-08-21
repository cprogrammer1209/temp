You are a helpful assistant. From the content provided by user populate the json, if value not present leave it empty.
     Table data can span across multiple pages too.The content provided by the user is Indian invoice.
 {"Invoice Details": [{"InvoiceSLNo": "Give the numuber according to the invoice document, like if there are 4 invoice document, numuber them with 1, 2, 3, 4", "InvoiceNo": "Extract the 'INVOICE NUMBER' from the document, which is typically formatted as a series of digits following the label 'INVOICE NUMBER'.", "InvoiceDate": "Extract the 'SHIP DATE' from the document, which indicates the date of the invoice.", "QtyCode": "Extract the quantity code for each item listed in the document, It will in the quantity column along with  the quantity. Quantity code will be LIke 'EA','PCS'", "Currency": "Extract the currency information from the document, typically found in the payment terms section, which may be indicated as 'CUR' or 'Currency' followed by the currency code (e.g., USD, EUR).", "Terms": "Extract the 'Payment Terms' from the document, It is a 3 letter word, it will present in the terms of payment or payment terms. It includes information such as 'DAP' or 'FCA' or 'FOC' or 'CPT' or similar terms. ", "InvoiceValue": "Extract the total invoice value from the document, which is typically found in the section labeled 'TOTAL' or 'SUBTOTAL' and is usually followed by a currency designation.", "SupplierName": "Extract the supplier name from the document, which is typically found in the section labeled 'SHIPPED FROM' or 'BILL FROM'.", "SupplierAdd1": "Extract the supplier address line from the document, and give only the first line of it(since we splitter the address into 4 line) , which is typically found under the 'SHIPPED FROM' section, following the company name.", "SupplierAdd2": "Extract the supplier address  from the document and give only the 2nd line of it(since we splitter the address into 4 line) ,, which is typically found under the 'SHIPPED FROM' section, following the company name.", "SupplierAdd3": "Extract the supplier address  from the document,  and give only the 3rd line of it(since we splitter the address into 4 line) , which is typically found under the 'SHIPPED FROM' section, following the company name.", "SupplierAdd4": "Extract the supplier address  from the document,  and give only the 4th line of it(since we splitter the address into 4 line) , which is typically found under the 'SHIPPED FROM' section or related words, following the company name."}], "Item Details": [{"InvoiceSlNo": "Number this sl no according to the order of invoice documnets. If there are 4 documents, and the line items from 3 invoice means, then it is 3", "itemSlNo": "Number this sl no according to the order of the line items. If there are 4 line items in the table, and the line items from 2 invoice means, then it is 2", "ItemDesc": "Extract the product description from the document, which is typically found under the 'PRODUCT DESCRIPTION' section and may include details such as the item name, specifications, and any relevant identifiers.", "Quantity": "Extract the 'Quantity Shipped' from the document, which is typically listed next to the item description and is represented as a numerical value.", "Rate": "Extract the 'Rate' information from the provided RC document, ensuring to look for any mention of pricing or rates associated with items, typically found in sections detailing unit price or extended price.", "Amount": "Extract the total amount from the document, typically found in the section labeled 'TOTAL' or 'TOTAL # OF ITEMS SHIPPED', and ensure to capture the numerical value following this label.", "PartNo": "Extract the Part Number (PartNo) from the document, which is typically indicated by 'PN:' followed by the alphanumeric code.", "PONumber": "Extract the Purchase Order Number (PO Number) from the document, which is typically labeled as 'CUST PO NUM' and is followed by a numeric value.", "ItemNETWEIGHT": "Extract the 'Item NET WEIGHT' from the document, ensuring to identify the relevant section where the item details are listed, typically following the 'ITEM' and 'QUANTITY SHIPPED' headings.", "ItemHSCODE": "Extract the Item HS Code from the document, which is typically found in the  product description and may be labeled as 'HTS Code' or 'HSCODE' . Some times, the description may span across in the next page", "ItemCountry": "Extract the country of origin for each line item listed in the document, specifically looking for the 'COO' (Country of Origin) information associated with each line item. The 'coo' or country of origin will be in the end of the each row description."}]}
 		    M67S AE43 J013J PES
 	       NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 			 NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			      CHANGXING, ZHEJIANG 313100 CHINA.
 				     FAX:0086-572-6210777
 					 R#
 					 INVOICE
 TO: GODREJ & BOYCE MFG. CO. LTD.		     R#S
     GALA NO. H10 TO H12, SAI DHARA,    INVOICE NO.: SP20250269
     MUMBAI-NASHIK HIGHWAY (NH3), BOROLI (KUKSE)
 						   8#
      VILLAGE, BHIWANDI, THANE :- 421302.
 						   DATE: MAR.20,2025
 						   AST4
 						   S/C NO.: KV1010913,KV1010853,KV1010929
 #MO#			    EKt		       1EH uF 5W
 FROM: CHONGQING		TO:  India		L/ C No.:
      #X				WESAY			      1r	  61
 SHIPPING MARKS  QUANTITIES AND DESCRIPTIONS			    PRICE      AMOUNT
 									     EXW India
 	    KV1010913
 	     SPARE PARTS
 	     PTE15N,#508098520001 brush holder	    4PCS USD3.22       USD12.88
 	     PTE15N,#502317020000 connecting plate      10PCS USD1.12	USD11.20
 	     RT15DP,#920200400056 proximity switch	 1PC USD4.19       USD4.19
 	     RT15DP,#214533510002 proximity switch Speed Limit 1PC USD14.54  USD14.54
 	     PSB12,#1000114017 left button		 1PC USD4.88       USD4.88
 	     PSB12,#9000008519 key			 1PC USD0.55       USD0.55
 	     PSB12,#9000008327 switch NBN5-F7-E5	  1PC USD14.21       USD14.21
 	     PSB12,#1000114015 horn button		 1PC USD1.05       USD1.05
 	     PSB12,#9000008332 magnetic switch-HWK2	1PC USD5.37       USD5.37
 	     PSB12,#9000008846 brake		       1PC USD82.62      USD82.62
 	     PSB12,#9000008858 internal gear	      1PC USD137.78     USD137.78
 	     PTE15N,#508098520018 belly seat	      2PCS USD0.52       USD1.04
 	     AC,#315 bearing			      5PCS USD3.23       USD16.15
 	     AC,#328 piston rod			   5PCS USD6.75       USD33.75
 	     PTE15N,#508098520001 brush holder	    2PCS USD3.22       USD6.44
 	     PSB12:#0000027001 bearing 6204	       6PCS USD0.98       USD5.88
 	     PTE15N,#502317020000 connecting plate	4PCS USD1.12       USD4.48
 	     PTE15N:#502398510015 small wheel assy	4PCS USD3.54       USD14.16
 	     PTE15N:#920200400056 proximity switch	 1PC USD4.19       USD4.19
 	     KV1010853
 	     SPARE PARTS
 	     DF,#DF20-04 load roller assy single type    2PCS USD10.12       USD20.24
 	     DF,#DF20-05 load roller assy tandem type     4PCS USD9.11       USD36.44
 	     DF,#DF20-08 bracket assy		      1PC USD4.46       USD4.46
 	     FE4P50Q,#256513011001 rim assembly 7.50V-15 2PCS USD82.57      USD165.14
 	     FE4P50Q,#256615511001 rim assembly 6.50F-10 2PCS USD51.15      USD102.30
 	     FE4P50Q,#256513010001 drive wheel assembly 250-15 2PCS USD273.17 USD546.34
 						 ##
 	     FE4P50Q,#256513011010 tire 250-15 solid front tyre 2PCS USD326.26 USD652.52
 						  NOBLELIFT INTELLISRG
 	     FE4P50Q,#255013010003 tire 23*9-10 solid rear tyre 2PCS USD169.21 USD338.42
 							       2PCS USD169.21
 ---PAGE END---		    MbS AE43 J13 PB0S
 	       NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 			 NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			      CHANGXING, ZHEJIANG 313100 CHINA.
 				     FAX:0086-572-6210777
 					R
 					INVOICE
 TO: GODREJ & BOYCE MFG. CO. LTD.		    R#S
     GALA NO. H10 TO H12, SAI DHARA,   INVOICE NO.: SP20250269
     MUMBAI-NASHIK HIGHWAY (NH3), BOROLI (KUKSE)
 						  8 #J
     VILLAGE, BHIWANDI, THANE :- 421302.
 						  DATE: MAR.20,2025
 						  AW8T4
 						  S/C NO.: KV1010913,KV1010853,KV1010929
 WOH			      EK		      1EH uF SW
 FROM: CHONGQING	       TO:  India		L/ C No.:
 	     FE4P50Q,#256615510001 rear tire assembly 23*9-10 2PCS USD169.21 USD338.42
 	    KV1010929
 	    SPARE PARTS
 	     PTE15N,#508011010002 Welding Fixed Shaft     1PC USD1.13       USD1.13
 	     PTE15N,#508011020005 Holder		  1PC USD0.36       USD0.36
 	     PTE15N,#910401300006 Shaft Circlip	   1PC USD0.01      USD0.01
 	     PSB12,#2000300004, Filter		  3PCS USD12.39      USD37.17
 	     AC,#B212 Pushing Rod Type		  2PCS USD7.14       USD14.28
 	     AC,#320 Elastic			   10PCS USD0.14	USD1.40
 	     RT15DP,#921100100145 Camera		 1PC USD216.60    USD216.60
 	     FE4P50Q,#256625011002 Multiple valve (triple mast) 1PC USD182.40 USD182.40
 	     RT15DP,#214553020143 Spring		2PCS USD0.50	USD1.00
 TOTAL:							  93PCS     USD3,033.99
 SAY TOTAL USD THREE THOUSAND THIRTY THREE AND NINETY NINE CENTS ONLY.
 REMARK: PLEASE NOTE THAT THE MONEY RECEIVED IN NOBLELIFT'S BANK ACCOUNT SHOULD BE THE
 EXACTLY SAME AMOUNT AS THE INVOICE VALUE.
 						#
 						 NOBLELIFT INTELLIGENT EQUIPMENT CO.LTD
 ---PAGE END---		 M7%S AE43J13PB0a
 	      NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 		    NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			 CHANGXING, ZHEJIANG 313100 CHINA.
 			      FAX:0086-572-6210777
 				# 10 4
 			     PACKING LIST
 			 (WEIGHT & MEASUREMENT LIST)
 MARKS & NUMBERS			  RHS
 AS PER INVOICE	    INVOICE NO.: SP20250269
 					8#
 					DATE: MAR.20,2025
 					AWS9:
 					S/C NO. KV1010913,KV1010853,KV1010929
 ART.NO: DESCRIPTION:       QUANTITY: PACKAGES:   G.W.   N. W. MEASUREMENT
 KV1010913
 SPARE PARTS
 PTE15N,#508098520001 brush holder 4PCS
 PTE15N,#502317020000 connecting plate 10PCS
 RT15DP,#920200400056 proximity switch 1PC
 RT15DP,#214533510002 proximity switch
 Speed Limit		     1PC
 PSB12,#1000114017 left button   1PC
 PSB12,#9000008519 key	   1PC
 PSB12,#9000008327 switch NBN5-F7-E5 1PC
 PSB12,#1000114015 horn button   1PC
 PSB12,#9000008332 magnetic switch-HWK2 1PC
 PSB12,#9000008846 brake	 1PC
 PSB12,#9000008858 internal gear 1PC
 PTE15N,#508098520018 belly seat 2PCS
 AC,#315 bearing		5PCS
 AC,#328 piston rod	     5PCS
 PTE15N,#508098520001 brush holder 2PCS
 PSB12:#0000027001 bearing 6204 6PCS
 PTE15N,#502317020000 connecting plate 4PCS
 PTE15N:#502398510015 small wheel assy 4PCS
 PTE15N:#920200400056 proximity switch 1PC 1CTN 26.2KGS  24KGS.  0.03CBM
 DF,#DF20-04 load roller assy single type 2PCS
 DF,#DF20-05 load roller assy tandem type 4PCS
 DF,#DF20-08 bracket assy	1PC		##1
 FE4P50Q,#256513011001 rim assembly NOBLELIFT INTELLIGENT EQUIPMENT CO.TD
 				2PCS
 7.50V-15
 ---PAGE END---		   M 7S AE48 J13 PBDS
 	       NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 		       NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			   CHANGXING, ZHEJIANG 313100 CHINA.
 				  FAX:0086-572-6210777
 				   # 4 4
 				PACKING LIST
 			    (WEIGHT & MEASUREMENT LIST)
 MARKS & NUMBERS			      RHS
 AS PER INVOICE		  INVOICE NO.: SP20250269
 					    8#
 					    DATE: MAR.20,2025
 					    A459:
 					    S/C NO. KV1010913,KV1010853,KV1010929
 FE4P50Q,#256615511001 rim assembly
 				    2PCS
 6.50F-10
 FE4P50Q,#256513010001 drive wheel
 				    2PCS
 assembly 250-15
 FE4P50Q,#256513011010 tire 250-15 solid
 				   2PCS
 front tyre
 FE4P50Q,#255013010003 tire 23*9-10 solid
 				    2PCS
 rear tyre
 FE4P50Q,#256615510001 rear tire assembly
 23*9-10			   2PCS       1PLT    654KGS   634KGS    1.72CBM
 PTE15N,#508011010002 Welding Fixed Shaft 1PC
 PTE15N,#508011020005 Holder	 1PC
 PTE15N,#910401300006 Shaft Circlip  1PC
 PSB12,#2000300004, Filter	  3PCS
 AC,#B212 Pushing Rod Type	  2PCS
 AC,#320 Elastic		   10PCS
 RT15DP,#921100100145 Camera	 1PC
 FE4P50Q,#256625011002 Multiple valve (triple
 mast)			       1PC      1CTN     13KGS    11KGS   0.01CBM
 RT15DP,#214553020143 Spring       2PCS       1CTN    5.8KGS     4KGS   0.01CBM
 			  TOTAL:  93PCS     4PKGS    699KGS   673KGS   1.77CBM
 SAY TOTAL FOUR PALLETS ONLY.
 					     #
 					     NOBLELIFT INTELLIGENT EQUIPMENT CO. LTD
 ---PAGE END---
                             You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                             Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                             Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                             ***Sample OCR data*** : 
             		    M67S AE43 J013J PES
 	       NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 			 NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			      CHANGXING, ZHEJIANG 313100 CHINA.
 				     FAX:0086-572-6210777
 					 R#
 					 INVOICE
 TO: GODREJ & BOYCE MFG. CO. LTD.		     R#S
     GALA NO. H10 TO H12, SAI DHARA,    INVOICE NO.: SP20250269
     MUMBAI-NASHIK HIGHWAY (NH3), BOROLI (KUKSE)
 						   8#
      VILLAGE, BHIWANDI, THANE :- 421302.
 						   DATE: MAR.20,2025
 						   AST4
 						   S/C NO.: KV1010913,KV1010853,KV1010929
 #MO#			    EKt		       1EH uF 5W
 FROM: CHONGQING		TO:  India		L/ C No.:
      #X				WESAY			      1r	  61
 SHIPPING MARKS  QUANTITIES AND DESCRIPTIONS			    PRICE      AMOUNT
 									     EXW India
 	    KV1010913
 	     SPARE PARTS
 	     PTE15N,#508098520001 brush holder	    4PCS USD3.22       USD12.88
 	     PTE15N,#502317020000 connecting plate      10PCS USD1.12	USD11.20
 	     RT15DP,#920200400056 proximity switch	 1PC USD4.19       USD4.19
 	     RT15DP,#214533510002 proximity switch Speed Limit 1PC USD14.54  USD14.54
 	     PSB12,#1000114017 left button		 1PC USD4.88       USD4.88
 	     PSB12,#9000008519 key			 1PC USD0.55       USD0.55
 	     PSB12,#9000008327 switch NBN5-F7-E5	  1PC USD14.21       USD14.21
 	     PSB12,#1000114015 horn button		 1PC USD1.05       USD1.05
 	     PSB12,#9000008332 magnetic switch-HWK2	1PC USD5.37       USD5.37
 	     PSB12,#9000008846 brake		       1PC USD82.62      USD82.62
 	     PSB12,#9000008858 internal gear	      1PC USD137.78     USD137.78
 	     PTE15N,#508098520018 belly seat	      2PCS USD0.52       USD1.04
 	     AC,#315 bearing			      5PCS USD3.23       USD16.15
 	     AC,#328 piston rod			   5PCS USD6.75       USD33.75
 	     PTE15N,#508098520001 brush holder	    2PCS USD3.22       USD6.44
 	     PSB12:#0000027001 bearing 6204	       6PCS USD0.98       USD5.88
 	     PTE15N,#502317020000 connecting plate	4PCS USD1.12       USD4.48
 	     PTE15N:#502398510015 small wheel assy	4PCS USD3.54       USD14.16
 	     PTE15N:#920200400056 proximity switch	 1PC USD4.19       USD4.19
 	     KV1010853
 	     SPARE PARTS
 	     DF,#DF20-04 load roller assy single type    2PCS USD10.12       USD20.24
 	     DF,#DF20-05 load roller assy tandem type     4PCS USD9.11       USD36.44
 	     DF,#DF20-08 bracket assy		      1PC USD4.46       USD4.46
 	     FE4P50Q,#256513011001 rim assembly 7.50V-15 2PCS USD82.57      USD165.14
 	     FE4P50Q,#256615511001 rim assembly 6.50F-10 2PCS USD51.15      USD102.30
 	     FE4P50Q,#256513010001 drive wheel assembly 250-15 2PCS USD273.17 USD546.34
 						 ##
 	     FE4P50Q,#256513011010 tire 250-15 solid front tyre 2PCS USD326.26 USD652.52
 						  NOBLELIFT INTELLISRG
 	     FE4P50Q,#255013010003 tire 23*9-10 solid rear tyre 2PCS USD169.21 USD338.42
 							       2PCS USD169.21
 ---PAGE NO: 1. END OF PAGE---		    MbS AE43 J13 PB0S
 	       NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 			 NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			      CHANGXING, ZHEJIANG 313100 CHINA.
 				     FAX:0086-572-6210777
 					R
 					INVOICE
 TO: GODREJ & BOYCE MFG. CO. LTD.		    R#S
     GALA NO. H10 TO H12, SAI DHARA,   INVOICE NO.: SP20250269
     MUMBAI-NASHIK HIGHWAY (NH3), BOROLI (KUKSE)
 						  8 #J
     VILLAGE, BHIWANDI, THANE :- 421302.
 						  DATE: MAR.20,2025
 						  AW8T4
 						  S/C NO.: KV1010913,KV1010853,KV1010929
 WOH			      EK		      1EH uF SW
 FROM: CHONGQING	       TO:  India		L/ C No.:
 	     FE4P50Q,#256615510001 rear tire assembly 23*9-10 2PCS USD169.21 USD338.42
 	    KV1010929
 	    SPARE PARTS
 	     PTE15N,#508011010002 Welding Fixed Shaft     1PC USD1.13       USD1.13
 	     PTE15N,#508011020005 Holder		  1PC USD0.36       USD0.36
 	     PTE15N,#910401300006 Shaft Circlip	   1PC USD0.01      USD0.01
 	     PSB12,#2000300004, Filter		  3PCS USD12.39      USD37.17
 	     AC,#B212 Pushing Rod Type		  2PCS USD7.14       USD14.28
 	     AC,#320 Elastic			   10PCS USD0.14	USD1.40
 	     RT15DP,#921100100145 Camera		 1PC USD216.60    USD216.60
 	     FE4P50Q,#256625011002 Multiple valve (triple mast) 1PC USD182.40 USD182.40
 	     RT15DP,#214553020143 Spring		2PCS USD0.50	USD1.00
 TOTAL:							  93PCS     USD3,033.99
 SAY TOTAL USD THREE THOUSAND THIRTY THREE AND NINETY NINE CENTS ONLY.
 REMARK: PLEASE NOTE THAT THE MONEY RECEIVED IN NOBLELIFT'S BANK ACCOUNT SHOULD BE THE
 EXACTLY SAME AMOUNT AS THE INVOICE VALUE.
 						#
 						 NOBLELIFT INTELLIGENT EQUIPMENT CO.LTD
 ---PAGE NO: 2. END OF PAGE---		 M7%S AE43J13PB0a
 	      NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 		    NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			 CHANGXING, ZHEJIANG 313100 CHINA.
 			      FAX:0086-572-6210777
 				# 10 4
 			     PACKING LIST
 			 (WEIGHT & MEASUREMENT LIST)
 MARKS & NUMBERS			  RHS
 AS PER INVOICE	    INVOICE NO.: SP20250269
 					8#
 					DATE: MAR.20,2025
 					AWS9:
 					S/C NO. KV1010913,KV1010853,KV1010929
 ART.NO: DESCRIPTION:       QUANTITY: PACKAGES:   G.W.   N. W. MEASUREMENT
 KV1010913
 SPARE PARTS
 PTE15N,#508098520001 brush holder 4PCS
 PTE15N,#502317020000 connecting plate 10PCS
 RT15DP,#920200400056 proximity switch 1PC
 RT15DP,#214533510002 proximity switch
 Speed Limit		     1PC
 PSB12,#1000114017 left button   1PC
 PSB12,#9000008519 key	   1PC
 PSB12,#9000008327 switch NBN5-F7-E5 1PC
 PSB12,#1000114015 horn button   1PC
 PSB12,#9000008332 magnetic switch-HWK2 1PC
 PSB12,#9000008846 brake	 1PC
 PSB12,#9000008858 internal gear 1PC
 PTE15N,#508098520018 belly seat 2PCS
 AC,#315 bearing		5PCS
 AC,#328 piston rod	     5PCS
 PTE15N,#508098520001 brush holder 2PCS
 PSB12:#0000027001 bearing 6204 6PCS
 PTE15N,#502317020000 connecting plate 4PCS
 PTE15N:#502398510015 small wheel assy 4PCS
 PTE15N:#920200400056 proximity switch 1PC 1CTN 26.2KGS  24KGS.  0.03CBM
 DF,#DF20-04 load roller assy single type 2PCS
 DF,#DF20-05 load roller assy tandem type 4PCS
 DF,#DF20-08 bracket assy	1PC		##1
 FE4P50Q,#256513011001 rim assembly NOBLELIFT INTELLIGENT EQUIPMENT CO.TD
 				2PCS
 7.50V-15
 ---PAGE NO: 3. END OF PAGE---		   M 7S AE48 J13 PBDS
 	       NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.
 		       NO.528 CHANGZHOU ROAD, TAIHU SUB-DISTRICT,
 			   CHANGXING, ZHEJIANG 313100 CHINA.
 				  FAX:0086-572-6210777
 				   # 4 4
 				PACKING LIST
 			    (WEIGHT & MEASUREMENT LIST)
 MARKS & NUMBERS			      RHS
 AS PER INVOICE		  INVOICE NO.: SP20250269
 					    8#
 					    DATE: MAR.20,2025
 					    A459:
 					    S/C NO. KV1010913,KV1010853,KV1010929
 FE4P50Q,#256615511001 rim assembly
 				    2PCS
 6.50F-10
 FE4P50Q,#256513010001 drive wheel
 				    2PCS
 assembly 250-15
 FE4P50Q,#256513011010 tire 250-15 solid
 				   2PCS
 front tyre
 FE4P50Q,#255013010003 tire 23*9-10 solid
 				    2PCS
 rear tyre
 FE4P50Q,#256615510001 rear tire assembly
 23*9-10			   2PCS       1PLT    654KGS   634KGS    1.72CBM
 PTE15N,#508011010002 Welding Fixed Shaft 1PC
 PTE15N,#508011020005 Holder	 1PC
 PTE15N,#910401300006 Shaft Circlip  1PC
 PSB12,#2000300004, Filter	  3PCS
 AC,#B212 Pushing Rod Type	  2PCS
 AC,#320 Elastic		   10PCS
 RT15DP,#921100100145 Camera	 1PC
 FE4P50Q,#256625011002 Multiple valve (triple
 mast)			       1PC      1CTN     13KGS    11KGS   0.01CBM
 RT15DP,#214553020143 Spring       2PCS       1CTN    5.8KGS     4KGS   0.01CBM
 			  TOTAL:  93PCS     4PKGS    699KGS   673KGS   1.77CBM
 SAY TOTAL FOUR PALLETS ONLY.
 					     #
 					     NOBLELIFT INTELLIGENT EQUIPMENT CO. LTD
 ---PAGE NO: 4. END OF PAGE---
             
                             *** Expected JSON Output *** : {'InvoiceDetails': [{'Currency': 'USD', 'InvoiceDate': 'MAR.20,2025', 'InvoiceNo': 'SP20250269', 'InvoiceSlNo': 1, 'InvoiceValue': '3,033.99', 'QtyCode': 'PCS', 'SupplierAdd1': 'NO.528 CHANGZHOU ROAD,', 'SupplierAdd2': 'TAIHU SUB-DISTRICT,', 'SupplierAdd3': 'VILLAGE, BHIWANDI,', 'SupplierAdd4': 'ZHEJIANG 313100 CHINA.', 'SupplierName': 'NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.', 'Terms': '', 'TermsofPayment': ''}], 'ItemsDetails': [{'Amount': '12.88', 'InvoiceSlNo': 1, 'ItemCountry': '', 'ItemDesc': 'PTE15N,#508098520001 brush holder', 'ItemHSCODE': '', 'ItemNETWEIGHT': None, 'ItemSlNo': 1, 'PONumber': '', 'PartNo': None, 'Quantity': '4', 'Rate': '3.22'}, {'Amount': '11.20', 'InvoiceSlNo': 1, 'ItemCountry': '', 'ItemDesc': 'PTE15N,#502317020000 connecting plate', 'ItemHSCODE': '', 'ItemNETWEIGHT': None, 'ItemSlNo': 3, 'PONumber': '', 'PartNo': None, 'Quantity': '10', 'Rate': '1.12'}, {'Amount': '4.19', 'InvoiceSlNo': 1, 'ItemCountry': '', 'ItemDesc': 'RT15DP,#920200400056 proximity switch', 'ItemHSCODE': '', 'ItemNETWEIGHT': None, 'ItemSlNo': 4, 'PONumber': '', 'PartNo': None, 'Quantity': '1', 'Rate': '4.19'}]}
