from precisely import assert_that, contains_exactly


def test_can_get_all_molecules_from_root(builder, graphql):
    with builder:
        builder.add_molecule(chembl_id="CHEMBL42")
        builder.add_molecule(chembl_id="CHEMBL43")
        builder.add_molecule(chembl_id="CHEMBL44")

    query = """
        query {
            molecules {
                chemblId
            }
        }
    """

    response = graphql(query)

    assert_that(response["molecules"], contains_exactly(
        {"chemblId": "CHEMBL42"},
        {"chemblId": "CHEMBL43"},
        {"chemblId": "CHEMBL44"},
    ))
