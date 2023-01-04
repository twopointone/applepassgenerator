from models import ApplePass


class ApplePassGeneratorClient(object):
    def __init__(self, team_identifier, pass_type_identifier, organization_name):
        self.team_identifier = team_identifier
        self.pass_type_identifier = pass_type_identifier
        self.organization_name = organization_name

    def get_pass(self, card_info):
        apple_pass = ApplePass(
            card_info,
            pass_type_identifier=self.pass_type_identifier,
            organization_name=self.organization_name,
            team_identifier=self.team_identifier,
        )
        return apple_pass
