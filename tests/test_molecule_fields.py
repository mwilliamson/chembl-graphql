from precisely import assert_that, contains_exactly, is_mapping


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


def test_can_get_synonyms_of_molecule(builder, graphql):
    with builder:
        molecule_1 = builder.add_molecule(chembl_id="CHEMBL1")
        molecule_2 = builder.add_molecule(chembl_id="CHEMBL2")
        builder.add_molecule(chembl_id="CHEMBL3")

        builder.add_molecule_synonym(
            molecule=molecule_1,
            name="<synonym 1>",
        )
        builder.add_molecule_synonym(
            molecule=molecule_2,
            name="<synonym 2a>",
        )
        builder.add_molecule_synonym(
            molecule=molecule_2,
            name="<synonym 2b>",
        )

    query = """
        query {
            molecules {
                chemblId
                synonyms {
                    name
                }
            }
        }
    """

    response = graphql(query)

    assert_that(response["molecules"], contains_exactly(
        is_mapping({
            "chemblId": "CHEMBL1",
            "synonyms": contains_exactly(
                {"name": "<synonym 1>"},
            ),
        }),
        is_mapping({
            "chemblId": "CHEMBL2",
            "synonyms": contains_exactly(
                {"name": "<synonym 2a>"},
                {"name": "<synonym 2b>"},
            ),
        }),
        is_mapping({
            "chemblId": "CHEMBL3",
            "synonyms": contains_exactly(),
        }),
    ))
