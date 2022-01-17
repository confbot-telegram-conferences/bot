# from tests.factories import ConferenceFactory, message_context
# from app.models.repositories import ConferenceRepository
# from app.handlers.conference_show import ConferenceShowHandler
# from app.listeners import register


# TODO: It is failing in the translations
# def test_start(injector, context, clear_collections):
#     pass
# clear_collections(["conferences"])
# clear_collections(["user_conference_views"])
# register()
# repository: ConferenceRepository = injector.get(ConferenceRepository)
# conference = repository.insert(ConferenceFactory())
# context.message = message_context(text=f"/show_conference {str(conference._id)}")
# handler: ConferenceShowHandler = injector.get(ConferenceShowHandler)
# handler.start(context, repository)
