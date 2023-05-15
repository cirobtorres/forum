from ..test_base import ObjectsFactoryMixins, TestCase, User


class AccountBaseTestModels(ObjectsFactoryMixins, TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()


class AccountModelsTest(AccountBaseTestModels):
    
    def test_models_account_str_dunder_name(self):
        user:User = self.create_random_user()
        self.assertEqual(first=user.username, second=str(user.account))
    
    def test_models_account_img_resize(self):
        ...
    
    def test_models_account_img_delete_when_changed(self):  # coverage html NÃO contabilizou! Verificar
        user:User = self.create_random_user()
        old_img = user.account.img['url']
        new_img = self.randomized_img()
        user.account.img['url'] = new_img
        user.save()
        self.assertNotEqual(first=user.account.img, second=old_img)