// collection: aiqod-staging.additionalinfos
{
	"_id" : ObjectId("6626044100fbf80a5ac30f45"),
	"__v" : 0,
	"additionalInfo" : [
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "0",
			"label" : "Process",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Process",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "Default",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : "Process",
			"RuleName" : "",
			"TableName" : "",
			"childDependentFields" : [ ],
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "1",
			"label" : "Task",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Task",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : true,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "yes"
		},
		{
			"type" : "TEXTAREA",
			"id" : "2",
			"label" : "Task Description",
			"placeholder" : "Task Description",
			"required" : true,
			"maxLength" : null,
			"validators" : {
				"maxLength" : null
			},
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"value" : "",
			"hidden" : false,
			"name" : "Task Description",
			"inputType" : "textArea",
			"RuleName" : "",
			"inDependent" : "yes"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "3",
			"label" : "Department",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Department",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : true,
			"tabIndex" : null,
			"value" : "",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : "Department",
			"RuleName" : "",
			"TableName" : "Project",
			"childDependentFields" : [ "Project" ],
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "4",
			"label" : "Project",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Project",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : [ "ProjectName" ],
			"RuleName" : "",
			"TableName" : "AIQOD_Project",
			"parentDependentField" : "Department",
			"inDependent" : "yes"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "5",
			"label" : "Status",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Status",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : "Status",
			"RuleName" : "",
			"TableName" : "",
			"inDependent" : "no"
		},
		{
			"type" : "CHECKBOX",
			"id" : "6",
			"label" : "Autotransition to Next Status",
			"required" : false,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"name" : "Autotransition to Next Status",
			"RuleName" : "",
			"inDependent" : "no"
		},
		{
			"type" : "DATEPICKER",
			"id" : "7",
			"label" : "Start Date",
			"required" : true,
			"value" : "",
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"name" : "Start Date",
			"RuleName" : "",
			"inDependent" : "yes"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "8",
			"label" : "Priority",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Priority",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : true,
			"tabIndex" : null,
			"value" : "Low",
			"options" : [
				{
					"disabled" : false,
					"label" : "Urgent",
					"value" : "Urgent"
				},
				{
					"disabled" : false,
					"label" : "High",
					"value" : "High"
				},
				{
					"disabled" : false,
					"label" : "Medium",
					"value" : "Medium"
				},
				{
					"disabled" : false,
					"label" : "Low",
					"value" : "Low"
				}
			],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : "Priority",
			"RuleName" : "",
			"TableName" : "",
			"inDependent" : "yes"
		},
		{
			"type" : "DATEPICKER",
			"id" : "9",
			"label" : "Due Date",
			"required" : true,
			"value" : "",
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"name" : "Due Date",
			"RuleName" : "",
			"inDependent" : "yes"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "10",
			"label" : "Assign To",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Assign To",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : true,
			"tabIndex" : null,
			"value" : "",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : "Assign To",
			"RuleName" : "",
			"TableName" : "",
			"inDependent" : "yes"
		},
		{
			"type" : "INPUT",
			"id" : "11",
			"label" : "Attachment",
			"disabled" : false,
			"value" : [
				{
					"name" : "Attachment",
					"doc" : null,
					"docName" : ""
				}
			],
			"inputType" : "file",
			"hidden" : false,
			"name" : "Attachment",
			"inDependent" : "yes"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "12",
			"label" : "Reviewer",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Reviewer",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : false,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"FieldName" : "Reviewer",
			"RuleName" : "",
			"TableName" : "",
			"inDependent" : "no"
		},
		{
			"type" : "CHECKBOX",
			"id" : "13",
			"label" : "Reviewer Selection Locked",
			"required" : false,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"name" : "Reviewer Selection Locked",
			"RuleName" : "",
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : false,
			"id" : "14",
			"label" : "Include in Notifications",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "Include in Notifications",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : null,
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"options" : [ ],
			"type" : "SELECT",
			"filterable" : false,
			"multiple" : true,
			"placeholder" : "",
			"prefix" : null,
			"suffix" : null,
			"enableSelectAll" : false,
			"FieldName" : "IncludeinNotifications",
			"RuleName" : "",
			"TableName" : "",
			"inDependent" : "yes"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "15",
			"label" : "emails",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "emails",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "16",
			"label" : "combinedArray",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "combinedArray",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "17",
			"label" : "names",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "names",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "18",
			"label" : "signedinuser",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "signedinuser",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "19",
			"label" : "statusIndex",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "statusIndex",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "20",
			"label" : "combinedstatusobject",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "combinedstatusobject",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "21",
			"label" : "autostransition",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "autostransition",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "22",
			"label" : "isQueue",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "isQueue",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "23",
			"label" : "nextStatus",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "nextStatus",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "24",
			"label" : "indexelem",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "indexelem",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "25",
			"label" : "assignPro",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "assignPro",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "26",
			"label" : "owner",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "owner",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		},
		{
			"asyncValidators" : null,
			"errorMessages" : {
				"required" : "{{label}} is required."
			},
			"hidden" : true,
			"id" : "27",
			"label" : "previousStatus",
			"labelTooltip" : null,
			"controlTooltip" : null,
			"layout" : null,
			"name" : "previousStatus",
			"relations" : [ ],
			"updateOn" : null,
			"validators" : {
				"maxLength" : null
			},
			"disabled" : false,
			"additional" : null,
			"hint" : null,
			"required" : false,
			"tabIndex" : null,
			"value" : "",
			"autoComplete" : "on",
			"autoFocus" : false,
			"maxLength" : null,
			"minLength" : null,
			"placeholder" : "",
			"prefix" : null,
			"readOnly" : false,
			"spellCheck" : false,
			"suffix" : null,
			"list" : null,
			"type" : "INPUT",
			"accept" : null,
			"inputType" : "text",
			"mask" : "",
			"maskConfig" : {
				"suffix" : "",
				"prefix" : "",
				"thousandSeparator" : " ",
				"decimalMarker" : [ ".", "," ],
				"clearIfNotMatch" : false,
				"showTemplate" : false,
				"showMaskTyped" : false,
				"placeHolderCharacter" : "_",
				"dropSpecialCharacters" : true,
				"shownMaskExpression" : "",
				"separatorLimit" : "",
				"allowNegativeNumbers" : false,
				"validation" : true,
				"specialCharacters" : [
					"-",
					"/",
					"(",
					")",
					".",
					":",
					" ",
					"+",
					",",
					"@",
					"[",
					"]",
					"\"",
					"'"
				],
				"leadZeroDateTime" : false,
				"triggerOnMaskChange" : false,
				"maskFilled" : {
					"_isScalar" : false,
					"observers" : [ ],
					"closed" : false,
					"isStopped" : false,
					"hasError" : false,
					"thrownError" : null,
					"__isAsync" : false
				},
				"patterns" : {
					"0" : {
						"pattern" : {
							
						}
					},
					"9" : {
						"pattern" : {
							
						},
						"optional" : true
					},
					"X" : {
						"pattern" : {
							
						},
						"symbol" : "*"
					},
					"A" : {
						"pattern" : {
							
						}
					},
					"S" : {
						"pattern" : {
							
						}
					},
					"U" : {
						"pattern" : {
							
						}
					},
					"L" : {
						"pattern" : {
							
						}
					},
					"d" : {
						"pattern" : {
							
						}
					},
					"m" : {
						"pattern" : {
							
						}
					},
					"M" : {
						"pattern" : {
							
						}
					},
					"H" : {
						"pattern" : {
							
						}
					},
					"h" : {
						"pattern" : {
							
						}
					},
					"s" : {
						"pattern" : {
							
						}
					}
				}
			},
			"max" : null,
			"min" : null,
			"multiple" : null,
			"pattern" : null,
			"step" : null,
			"inDependent" : "no"
		}
	],
	"autofillpdfPath" : "",
	"colomns" : "2",
	"createdAt" : ISODate("2024-01-19T13:49:15.189+05:30"),
	"isDeleted" : false,
	"orgId" : ObjectId("5c495dbfffa2a85b2c19a77f"),
	"ruleId" : ObjectId("66d445327dd76f995ba6a48e"),
	"structure" : [
		{
			"id" : 1,
			"displayName" : "Process",
			"parameterName" : "Process",
			"type" : "dynamic dropdown",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : true,
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Process",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : false,
			"kanbandBoardDropDownOption" : true,
			"bulkupload" : true,
			"childDependentFields" : [ ],
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : -1,
			"displayName" : "Task",
			"parameterName" : "Task",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : true,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Task",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"addToTaskName" : false,
			"hidden" : false,
			"inDependent" : "yes",
			"KanbanBoardDisplay" : true,
			"kanbandBoardDropDownOption" : false,
			"bulkupload" : true,
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : 0,
			"displayName" : "Task Description",
			"parameterName" : "Task Description",
			"type" : "textArea",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : true,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "TaskDescription",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"addToTaskName" : false,
			"hidden" : false,
			"inDependent" : "yes",
			"kanbandBoardDropDownOption" : false,
			"KanbanBoardDisplay" : true,
			"bulkupload" : true
		},
		{
			"id" : 7,
			"displayName" : "Department",
			"parameterName" : "Department",
			"type" : "dynamic dropdown",
			"defaultValue" : true,
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"mandatoryField" : true,
			"options" : [ ],
			"TableName" : "Project",
			"FieldName" : "Department",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"addToTaskName" : false,
			"hidden" : false,
			"inDependent" : "no",
			"kanbandBoardDropDownOption" : true,
			"KanbanBoardDisplay" : true,
			"childDependentFields" : [ "Project" ],
			"bulkupload" : true,
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : 1,
			"displayName" : "Project",
			"parameterName" : "Project",
			"type" : "dynamicAdd",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "AIQOD_Project",
			"FieldName" : [ "ProjectName" ],
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"addToTaskName" : false,
			"hidden" : false,
			"inDependent" : "yes",
			"UIName" : [
				{
					"label" : "Project Name",
					"value" : "ProjectName"
				}
			],
			"kanbandBoardDropDownOption" : true,
			"dependentField" : "Department",
			"parentDependentField" : "Department",
			"bulkupload" : true,
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : 0,
			"displayName" : "Status",
			"parameterName" : "Status",
			"type" : "dynamic dropdown",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Status",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : false,
			"kanbandBoardDropDownOption" : true,
			"KanbanBoardDisplay" : true,
			"bulkupload" : true,
			"kanbanBoardBottransaction" : true,
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : 1,
			"displayName" : "Autotransition to Next Status",
			"parameterName" : "Autotransition to Next Status",
			"type" : "checkbox",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Autotransition to Next Status",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : false,
			"bulkupload" : true
		},
		{
			"id" : 1,
			"displayName" : "Start Date",
			"parameterName" : "Start Date",
			"type" : "date",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : true,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "StartDate",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "yes",
			"addToTaskName" : false,
			"hidden" : false,
			"kanbandBoardDropDownOption" : false,
			"KanbanBoardDisplay" : true,
			"bulkupload" : true
		},
		{
			"id" : 2,
			"displayName" : "Priority",
			"parameterName" : "Priority",
			"type" : "dropdown",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"mandatoryField" : true,
			"options" : [ "Urgent", "High", "Medium", "Low" ],
			"TableName" : "",
			"FieldName" : "Priority",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"addToTaskName" : false,
			"hidden" : false,
			"inDependent" : "yes",
			"kanbandBoardDropDownOption" : true,
			"KanbanBoardDisplay" : true,
			"bulkupload" : true,
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : 1,
			"displayName" : "Due Date",
			"parameterName" : "Due Date",
			"type" : "date",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : true,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "DueDate",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"addToTaskName" : false,
			"hidden" : false,
			"inDependent" : "yes",
			"kanbandBoardDropDownOption" : false,
			"KanbanBoardDisplay" : true,
			"bulkupload" : true
		},
		{
			"id" : 1,
			"displayName" : "Assign To",
			"parameterName" : "Assign To",
			"type" : "dynamic dropdown",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : false,
			"mandatoryField" : true,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Assign To",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "yes",
			"addToTaskName" : false,
			"hidden" : false,
			"kanbandBoardDropDownOption" : true,
			"KanbanBoardDisplay" : false,
			"bulkupload" : true,
			"kanbanBoardBottransaction" : true,
			"kanbandBoardSearchColumn" : true
		},
		{
			"id" : 1,
			"displayName" : "Attachment",
			"parameterName" : "Attachment",
			"type" : "attachment",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Attachment",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "yes",
			"addToTaskName" : false,
			"hidden" : false
		},
		{
			"id" : 2,
			"displayName" : "Reviewer",
			"parameterName" : "Reviewer",
			"type" : "dynamic dropdown",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "Reviewer",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : false,
			"kanbandBoardDropDownOption" : true,
			"bulkupload" : true,
			"kanbanBoardBottransaction" : true
		},
		{
			"id" : 1,
			"displayName" : "Reviewer Selection Locked",
			"parameterName" : "Reviewer Selection Locked",
			"type" : "checkbox",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : true,
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "ReviewerSelectionLocked",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "Include in Notifications",
			"parameterName" : "Include in Notifications",
			"type" : "dynamic multiselect",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "IncludeinNotifications",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "yes",
			"addToTaskName" : false,
			"hidden" : false,
			"bulkupload" : true
		},
		{
			"id" : 1,
			"displayName" : "emails",
			"parameterName" : "emails",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "emails",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 2,
			"displayName" : "combinedArray",
			"parameterName" : "combinedArray",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "combinedArray",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "names",
			"parameterName" : "names",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "names",
			"RuleName" : "",
			"showTabdrop" : true,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "signedinuser",
			"parameterName" : "signedinuser",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "signedinuser",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "statusIndex",
			"parameterName" : "statusIndex",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "statusIndex",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "combinedstatusobject",
			"parameterName" : "combinedstatusobject",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "combinedstatusobject",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "autostransition",
			"parameterName" : "autostransition",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "autostransition",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 2,
			"displayName" : "isQueue",
			"parameterName" : "isQueue",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "isQueue",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 3,
			"displayName" : "nextStatus",
			"parameterName" : "nextStatus",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "nextStatus",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "indexelem",
			"parameterName" : "indexelem",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "indexelem",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "assignPro",
			"parameterName" : "assignPro",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "assignPro",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "owner",
			"parameterName" : "owner",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "owner",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		},
		{
			"id" : 1,
			"displayName" : "previousStatus",
			"parameterName" : "previousStatus",
			"type" : "text",
			"inputType" : "",
			"inputLength" : null,
			"minimum" : 0,
			"maximum" : Long("999999999999999"),
			"defaultValue" : "",
			"mandatoryField" : false,
			"options" : [ ],
			"TableName" : "",
			"FieldName" : "previousStatus",
			"RuleName" : "",
			"showTabdrop" : false,
			"showFielddrop" : true,
			"childTable" : [ ],
			"lobId" : "",
			"addToTaskList" : false,
			"inDependent" : "no",
			"addToTaskName" : false,
			"hidden" : true
		}
	],
	"subscriberId" : ObjectId("5beaabd82ac6767c86dc311c"),
	"taskName" : "",
	"templateName" : "Collab Pro V5 Template",
	"type" : "template",
	"updatedAt" : ISODate("2025-04-03T18:57:44.089+05:30"),
	"userId" : ObjectId("5beaabd82ac6767c86dc311e")
}