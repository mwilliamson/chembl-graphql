from precisely import assert_that, contains_exactly


def test_can_get_scalar_fields_of_molecule(builder, graphql):
    with builder:
        builder.add_molecule(
            chembl_id="CHEMBL1",
            pref_name="<pref name 1>",
        )
        builder.add_molecule(
            chembl_id="CHEMBL2",
            pref_name="<pref name 2>",
        )

    query = """
        query {
            molecules {
                chemblId
                prefName
            }
        }
    """

    response = graphql(query)

    assert_that(response["molecules"], contains_exactly(
        {
            "chemblId": "CHEMBL1",
            "prefName": "<pref name 1>",
        },
        {
            "chemblId": "CHEMBL2",
            "prefName": "<pref name 2>",
        },
    ))
