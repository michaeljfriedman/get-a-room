# Appendix

Below we describe our workflow, code style, and policy regarding the code and documentation.

## Branches
We use a traditional branching workflow:

```
       master      dev  topic
         |          |     |
__________          |     |     production-ready
          \__________     |     project in development
                     \_____     topic in development
```

- Our `master` branch is the production-ready branch - i.e. the branch that is deployed for users. It is *fully working and tested*.
- Our `dev` branch runs ahead of `master` with our latest work on the app, and it is merged into `master` when it is ready to release to users (e.g. a new release version, a new set of features, etc.). Thus, there should be *no* direct commits to `master` - only merges from `dev`.
- Additionally, we use "topic branches" stemming from `dev` to work on individual features, and merge them back into `dev` when they are done. Name these branches with a 1-3 word summary of the topic, separated by hyphens, e.g. `new-side-panel`.

## Code Conventions
Any commits should abide by the following code conventions:

- General
  - Indentation: 4 spaces (*not tabs*)
  - Line endings: Unix-style LF (`\n`)
  - File headers: Provide at least the following information surrounded by lines of hyphens/asterisks: the name of the file, the author(s), and a description of the file.
    e.g. In Python:
    ```python
    #----------------------------------------------------------
    # sample.py
	# Author: Joe Smith
	#
	# A sample description.
	#----------------------------------------------------------
    ```
- Python-specific
  - Strings: Use single quotes
  - Header comments: Standard Python style. Immediately inside the function/class, enclosed in triple quotes, as shown below:
    ```python
    def f():
        '''
        Header comment
        '''
    ```

## Code and Documentation Update Policy
You can make changes to the code and push to the repository at will on *your topic branches*. However, you must review your changes with all members of the project (e.g. with a pull request) before merging to the `dev` branch. Likewise, merges to `master` will be carefully reviewed by all members of the project.

We keep the documentation in this repository along with the code so that it always serves as an accurate, up-to-date reference for the code. Thus, any changes made to the code should have corresponding changes to the documentation if necessary. We have designed the documentation so that changes to the code usually should not require changes to the documentation outside the existing framework (i.e. you should not need any additional pages and or sections within the existing pages). So try to keep your changes within this framework when it makes sense to do so. However, if you must add new pages, sections, etc. make sure to review those changes with the other members of the project.