from ..test_base import ObjectsFactoryMixins, TestCase, Tag


class TagTestModels(ObjectsFactoryMixins, TestCase):

    def test_model_tag_str_dunder_name(self):
        tag:Tag = self.create_random_tag(tag_name='This my Name at this Current Momment')
        self.assertEqual(first='This my Name at this Current Momment', second=str(tag))

    def test_model_tag_slug(self):
        tag:Tag = self.create_random_tag(tag_name='Tâg wíth Nõ Slúg Dëclàréd')
        self.assertTrue(expr='tag-with-no-slug-declared' in tag.slug)