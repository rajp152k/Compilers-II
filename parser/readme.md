# Parser Development Phase

## Grammar conventions(./fg.lark) : only what's non-obvious
 - fg : figure grammar : can change later
 - the grammar goes here

## Transformer(./transform)

 - all parse tree to execution transformations(functions) placed here.
 - use doc strings for all functions 

## Test cases (./tests)

 - naming convention : '{rule or feature that it tests:hyphenated}_test.fu'
 	- will number/group them later sensibly for placement in docs
 - place feature tests in './tests/features'
 - place rule tests in './tests/rules'

 # USAGE
```
python eval.py  	# picks a random file from tests and proceeds
python eval.py	--src relative_path # evaluate this file
```
