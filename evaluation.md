Evaluation Strategies
=====================

Strategies for determining whether the Attribute Grammar approach is a good one.

Hand Written Attributes
-----------------------

1. Expression of specific types of semantics
    1. Declare Before Use
    2. Type Agreement
    3. Size Agreement
    4. Ect...
    5. Issues
        1. Only confirms it does what we expect it too....
2. Code Coverage
    1. Does it achieve good coverage.
    2. Test against multiple implementations of the same language (courtesy
       293).
    3. Use branch coverage as well as line coverage
    4. Issues
        1. An imperfect metric for discussing how good the test cases are.
           However, it appears to be pervasively used in fuzz testing
           literature.
3. Finding Specific Vulnerabilities
    1. Identify several specific applications and associated vulnerabilities
    2. Confirm exploitability
    3. Write grammar intended to generate a test case for those vulnerabilities
    4. Confirm it will generate the vulnerability


Inferred Attributes
-------------------

1. All three from above
2. Comparing Coverage/Vulnerabilities Exercised in Examples vs. Generated
    1. Run the examples
    2. Run a generated corpus
    3. Look at overlap and the differences between the lines/branches covered
    4. Compare the vulnerabilities exercised/identified by the two corpuses
3. Attempt to find a new vulnerability/bug in some application.
    1. Eg. real test. Large program. Real corpus of examples gathered from the
       web
