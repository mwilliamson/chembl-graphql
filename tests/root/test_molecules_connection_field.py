from precisely import anything, assert_that, contains_exactly, is_mapping


def test_when_there_are_more_molecules_than_requested_then_first_molecules_are_fetched(builder, graphql):
    with builder:
        builder.add_molecule(chembl_id="CHEMBL42")
        builder.add_molecule(chembl_id="CHEMBL43")
        builder.add_molecule(chembl_id="CHEMBL44")

    query = """
        query {
            moleculesConnection(first: 2) {
                edges {
                    node {
                        chemblId
                    }
                }
                pageInfo {
                    hasNextPage
                }
            }
        }
    """

    response = graphql(query)

    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(
            is_mapping({"node": {"chemblId": "CHEMBL42"}}),
            is_mapping({"node": {"chemblId": "CHEMBL43"}}),
        ),
        "pageInfo": is_mapping({"hasNextPage": True}),
    }))


def test_when_there_are_fewer_molecules_than_requested_then_all_molecules_are_fetched(builder, graphql):
    with builder:
        builder.add_molecule(chembl_id="CHEMBL42")

    query = """
        query {
            moleculesConnection(first: 2) {
                edges {
                    node {
                        chemblId
                    }
                }
                pageInfo {
                    hasNextPage
                }
            }
        }
    """

    response = graphql(query)

    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(
            is_mapping({"node": {"chemblId": "CHEMBL42"}}),
        ),
        "pageInfo": is_mapping({"hasNextPage": False}),
    }))


def test_when_there_are_exactly_number_of_molecules_requested_then_all_molecules_are_fetched(builder, graphql):
    with builder:
        builder.add_molecule(chembl_id="CHEMBL42")
        builder.add_molecule(chembl_id="CHEMBL43")

    query = """
        query {
            moleculesConnection(first: 2) {
                edges {
                    node {
                        chemblId
                    }
                }
                pageInfo {
                    hasNextPage
                }
            }
        }
    """

    response = graphql(query)

    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(
            is_mapping({"node": {"chemblId": "CHEMBL42"}}),
            is_mapping({"node": {"chemblId": "CHEMBL43"}}),
        ),
        "pageInfo": is_mapping({"hasNextPage": False}),
    }))


def test_cursor_can_be_used_as_after_argument_to_get_next_page(builder, graphql):
    with builder:
        builder.add_molecule(chembl_id="CHEMBL42")
        builder.add_molecule(chembl_id="CHEMBL43")
        builder.add_molecule(chembl_id="CHEMBL44")
        builder.add_molecule(chembl_id="CHEMBL45")
        builder.add_molecule(chembl_id="CHEMBL46")

    query = """
        query ($after: String) {
            moleculesConnection(first: 2, after: $after) {
                edges {
                    node {
                        chemblId
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    """

    response = graphql(query, variables={"after": None})
    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(
            is_mapping({"node": {"chemblId": "CHEMBL42"}}),
            is_mapping({"node": {"chemblId": "CHEMBL43"}}),
        ),
        "pageInfo": is_mapping({"endCursor": anything, "hasNextPage": True}),
    }))

    response = graphql(query, variables={"after": response["moleculesConnection"]["pageInfo"]["endCursor"]})
    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(
            is_mapping({"node": {"chemblId": "CHEMBL44"}}),
            is_mapping({"node": {"chemblId": "CHEMBL45"}}),
        ),
        "pageInfo": is_mapping({"endCursor": anything, "hasNextPage": True}),
    }))

    response = graphql(query, variables={"after": response["moleculesConnection"]["pageInfo"]["endCursor"]})
    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(
            is_mapping({"node": {"chemblId": "CHEMBL46"}}),
        ),
        "pageInfo": is_mapping({"endCursor": anything, "hasNextPage": False}),
    }))

    response = graphql(query, variables={"after": response["moleculesConnection"]["pageInfo"]["endCursor"]})
    assert_that(response["moleculesConnection"], is_mapping({
        "edges": contains_exactly(),
        "pageInfo": is_mapping({"endCursor": None, "hasNextPage": False}),
    }))
